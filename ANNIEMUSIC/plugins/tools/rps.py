import asyncio
import random
from ANNIEMUSIC import app
from uuid import uuid4
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

pending_rps = {}          # {chat_id: {game_id: player1_user}}
rps_games = {}            # {chat_id: {game_id: {'player1', 'player2', 'choices'}}}
pending_messages = {}     # {chat_id: {game_id: message}}

def get_user_display(user):
    return f"@{user.username}" if user.username else user.first_name

def emoji(choice):
    return {
        'rock': '🪨',
        'paper': '📄',
        'scissors': '✂️'
    }.get(choice, '')

def determine_rps_winner(p1, p2):
    if p1 == p2:
        return 0
    outcomes = {
        ('rock', 'scissors'): 1,
        ('scissors', 'paper'): 1,
        ('paper', 'rock'): 1,
        ('scissors', 'rock'): 2,
        ('paper', 'scissors'): 2,
        ('rock', 'paper'): 2
    }
    return outcomes.get((p1, p2), 0)

@app.on_message(filters.command("rps"))
async def start_rps(client, message: Message):
    chat_id = message.chat.id
    player1 = message.from_user
    game_id = str(uuid4())

    pending_rps.setdefault(chat_id, {})[game_id] = player1

    msg = await message.reply(
        f"{get_user_display(player1)} started a Rock-Paper-Scissors game!\nChoose your mode:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👤 Play with a user", callback_data=f"join_rps:{game_id}")],
            [InlineKeyboardButton("🤖 Play with AI", callback_data=f"ai_rps:{game_id}")]
        ])
    )

    pending_messages.setdefault(chat_id, {})[game_id] = msg

    async def timeout():
        await asyncio.sleep(20)
        if game_id in pending_rps.get(chat_id, {}):
            try:
                await msg.edit_text("⌛ Game expired. No one joined in time.")
            except:
                pass
            pending_rps[chat_id].pop(game_id, None)
            pending_messages[chat_id].pop(game_id, None)

    asyncio.create_task(timeout())

@app.on_callback_query(filters.regex(r"join_rps:(.+)"))
async def join_rps(client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    player2 = callback_query.from_user
    game_id = callback_query.data.split(":")[1]

    player1 = pending_rps.get(chat_id, {}).get(game_id)
    if not player1:
        await callback_query.answer("❌ Game not found or already started.")
        return

    if player1.id == player2.id:
        await callback_query.answer("You can't join your own game!")
        return

    rps_games.setdefault(chat_id, {})[game_id] = {
        'player1': player1,
        'player2': player2,
        'choices': {}
    }

    # Clean pending
    pending_rps[chat_id].pop(game_id, None)
    pending_messages[chat_id].pop(game_id, None)

    await callback_query.message.edit_text(
        f"🎮 Game Started!\n"
        f"{get_user_display(player1)} vs {get_user_display(player2)}\n\n"
        f"Choose your move:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🪨 Rock", callback_data=f"rps_move:rock:{game_id}")],
            [InlineKeyboardButton("📄 Paper", callback_data=f"rps_move:paper:{game_id}")],
            [InlineKeyboardButton("✂️ Scissors", callback_data=f"rps_move:scissors:{game_id}")]
        ])
    )

# ✅ AI MODE HANDLER
@app.on_callback_query(filters.regex(r"ai_rps:(.+)"))
async def play_with_ai(client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    player = callback_query.from_user
    game_id = callback_query.data.split(":")[1]

    rps_games.setdefault(chat_id, {})[game_id] = {
        'player1': player,
        'player2': 'ai',
        'choices': {}
    }

    pending_rps[chat_id].pop(game_id, None)
    pending_messages[chat_id].pop(game_id, None)

    await callback_query.message.edit_text(
        f"🎮 Game Started vs AI!\n"
        f"{get_user_display(player)} vs 🤖 AI\n\n"
        f"Choose your move:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🪨 Rock", callback_data=f"rps_move:rock:{game_id}")],
            [InlineKeyboardButton("📄 Paper", callback_data=f"rps_move:paper:{game_id}")],
            [InlineKeyboardButton("✂️ Scissors", callback_data=f"rps_move:scissors:{game_id}")]
        ])
    )

@app.on_callback_query(filters.regex(r"rps_move:(rock|paper|scissors):(.+)"))
async def handle_move(client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    user = callback_query.from_user
    move, game_id = callback_query.data.split(":")[1:]

    game = rps_games.get(chat_id, {}).get(game_id)
    if not game:
        await callback_query.answer("❌ No active game.")
        return

    if game['player2'] == 'ai':
        if user.id != game['player1'].id:
            await callback_query.answer("You're not a player in this game.")
            return

        game['choices'][user.id] = move
        await callback_query.answer("✅ Move registered.")

        ai_move = random.choice(['rock', 'paper', 'scissors'])
        game['choices']['ai'] = ai_move

        m1 = game['choices'][user.id]
        m2 = ai_move

        result_text = (
            f"{get_user_display(user)} chose {emoji(m1)}\n"
            f"🤖 AI chose {emoji(m2)}\n\n"
        )

        winner = determine_rps_winner(m1, m2)

        if winner == 0:
            result_text += "🤝 It's a draw!"
        elif winner == 1:
            result_text += f"🎉 {get_user_display(user)} wins!"
        else:
            result_text += "🤖 AI wins!"

        try:
            await callback_query.message.edit_text(result_text)
        except:
            pass

        rps_games[chat_id].pop(game_id, None)
        return

    # Multiplayer mode logic
    if user.id not in [game['player1'].id, game['player2'].id]:
        await callback_query.answer("You're not a player in this game.")
        return

    if user.id in game['choices']:
        await callback_query.answer("You've already made your move.")
        return

    game['choices'][user.id] = move
    await callback_query.answer("✅ Move registered.")

    if len(game['choices']) == 2:
        p1 = game['player1']
        p2 = game['player2']
        m1 = game['choices'][p1.id]
        m2 = game['choices'][p2.id]

        result_text = (
            f"{get_user_display(p1)} chose {emoji(m1)}\n"
            f"{get_user_display(p2)} chose {emoji(m2)}\n\n"
        )

        winner = determine_rps_winner(m1, m2)

        if winner == 0:
            result_text += "🤝 It's a draw!"
        elif winner == 1:
            result_text += f"🎉 {get_user_display(p1)} wins!"
        else:
            result_text += f"🎉 {get_user_display(p2)} wins!"

        try:
            await callback_query.message.edit_text(result_text)
        except:
            pass

        rps_games[chat_id].pop(game_id, None)
