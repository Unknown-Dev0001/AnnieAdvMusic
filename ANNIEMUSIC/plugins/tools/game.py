from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ANNIEMUSIC import app
import random

# Game states
pending_games = {}  # {chat_id: player_x}
games = {}  # {chat_id: TicTacToe instance}


def get_user_identity(user):
    return f"@{user.username}" if user.username else user.first_name


class TicTacToe:
    def __init__(self, player_x, player_o):
        self.board = [' ' for _ in range(9)]
        self.player_x = player_x
        self.player_o = player_o
        self.current_turn = player_x
        self.symbols = {player_x: '❌', player_o: '⭕'}
        self.winner = None

    def make_move(self, player, pos):
        if player != self.current_turn or self.board[pos] != ' ':
            return False

        self.board[pos] = self.symbols[player]
        if self.check_win(self.symbols[player]):
            self.winner = player
        elif ' ' not in self.board:
            self.winner = 'draw'
        else:
            self.current_turn = self.player_o if player == self.player_x else self.player_x
        return True

    def check_win(self, sym):
        win_pos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        return any(all(self.board[i] == sym for i in combo) for combo in win_pos)

    def render_buttons(self):
        def cell(i):
            return self.board[i] if self.board[i] != ' ' else '🟦'

        buttons = [
            [InlineKeyboardButton(cell(i), callback_data=f"move_{i}") for i in row]
            for row in [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
        ]
        return InlineKeyboardMarkup(buttons)

    def status_text(self):
        if self.winner == 'draw':
            return "🤝 It's a draw!"
        elif self.winner:
            return f"🎉 {self.symbols[self.winner]} ({self.winner}) wins!"
        else:
            return f"{self.symbols[self.current_turn]}'s turn ({self.current_turn})"


def ai_make_move(game: TicTacToe):
    available = [i for i, cell in enumerate(game.board) if cell == ' ']
    return random.choice(available) if available else None


async def start_game_function(chat_id, player_x, message):
    pending_games[chat_id] = player_x

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Join Game (PvP)", callback_data="join_game")],
        [InlineKeyboardButton("Play with AI", callback_data="play_ai")]
    ])
    await message.reply(
        f"{player_x} started a game of Tic Tac Toe!\nChoose an option below:",
        reply_markup=buttons
    )


@app.on_message(filters.command("ttt"))
async def start_game(client, message: Message):
    chat_id = message.chat.id
    player_x = get_user_identity(message.from_user)
    await start_game_function(chat_id, player_x, message)


@app.on_callback_query(filters.regex("join_game"))
async def join_game(client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    if chat_id not in pending_games:
        await callback_query.answer("No pending game to join.")
        return

    player_x = pending_games[chat_id]
    player_o = get_user_identity(callback_query.from_user)

    if player_o == player_x:
        await callback_query.answer("You can't join your own game!")
        return

    game = TicTacToe(player_x, player_o)
    games[chat_id] = game
    pending_games.pop(chat_id)

    await callback_query.message.edit_text(
        f"Tic Tac Toe: {player_x} (❌) vs {player_o} (⭕)\n{player_x}'s turn!",
        reply_markup=game.render_buttons()
    )


@app.on_callback_query(filters.regex("play_ai"))
async def play_with_ai(client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    player_x = pending_games.pop(chat_id, None)
    player_o = "AI 🤖"

    if not player_x:
        await callback_query.answer("No pending game found.")
        return

    game = TicTacToe(player_x, player_o)
    games[chat_id] = game

    await callback_query.message.edit_text(
        f"Tic Tac Toe: {player_x} (❌) vs {player_o} (⭕)\n{player_x}'s turn!",
        reply_markup=game.render_buttons()
    )


@app.on_callback_query(filters.regex(r"move_(\d)"))
async def handle_move(client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    user = get_user_identity(callback_query.from_user)

    if chat_id not in games:
        await callback_query.answer("No active game here.")
        return

    game = games[chat_id]
    pos = int(callback_query.data.split("_")[1])

    if not game.make_move(user, pos):
        await callback_query.answer("Invalid move or not your turn.")
        return

    text = game.status_text()
    await callback_query.message.edit_text(text, reply_markup=game.render_buttons())

    if game.winner:
        games.pop(chat_id)
        return

    if game.current_turn == "AI 🤖":
        ai_pos = ai_make_move(game)
        if ai_pos is not None:
            game.make_move("AI 🤖", ai_pos)
            text = game.status_text()
            await callback_query.message.edit_text(text, reply_markup=game.render_buttons())
            if game.winner:
                games.pop(chat_id)
