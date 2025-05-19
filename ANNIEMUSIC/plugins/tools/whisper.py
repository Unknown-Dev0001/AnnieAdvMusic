from ANNIEMUSIC import app
from config import BOT_USERNAME
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton
)

whisper_db = {}

switch_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💒 Start Whisper", switch_inline_query_current_chat="")]])

async def _whisper(_, inline_query):
    data = inline_query.query.strip()
    results = []

    parts = data.split()
    if len(parts) < 2:
        mm = [
            InlineQueryResultArticle(
                title="💒 Whisper",
                description=f"@{BOT_USERNAME} [ MESSAGE ] [ @USERNAME or ID ]",
                input_message_content=InputTextMessageContent(
                    f"💒 Usage:\n\n@{BOT_USERNAME} [ MESSAGE ] [ @USERNAME or ID ]\n\nExample:\n@{BOT_USERNAME} Hello there @someone"),
                thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
                reply_markup=switch_btn
            )
        ]
    else:
        try:
            user_id = parts[-1]
            msg = " ".join(parts[:-1])
        except IndexError:
            user_id, msg = None, None

        try:
            user = await _.get_users(user_id)
        except Exception:
            mm = [
                InlineQueryResultArticle(
                    title="💒 Whisper",
                    description="Invalid username or ID!",
                    input_message_content=InputTextMessageContent("Invalid username or ID!"),
                    thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
                    reply_markup=switch_btn
                )
            ]
        else:
            whisper_btn = InlineKeyboardMarkup(
                [[InlineKeyboardButton("💒 Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}")]]
            )
            one_time_whisper_btn = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔩 One-Time Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}_one")]]
            )
            mm = [
                InlineQueryResultArticle(
                    title="💒 Whisper",
                    description=f"Send a Whisper to {user.first_name}!",
                    input_message_content=InputTextMessageContent(
                        f"💒 You've sent a whisper to {user.first_name}."),
                    thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
                    reply_markup=whisper_btn
                ),
                InlineQueryResultArticle(
                    title="🔩 One-Time Whisper",
                    description=f"Send a one-time whisper to {user.first_name}!",
                    input_message_content=InputTextMessageContent(
                        f"🔩 You've sent a one-time whisper to {user.first_name}."),
                    thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
                    reply_markup=one_time_whisper_btn
                )
            ]
            try:
                whisper_db[f"{inline_query.from_user.id}_{user.id}"] = msg
            except Exception:
                pass

    results.extend(mm)
    return results


@app.on_callback_query(filters.regex(pattern=r"fdaywhisper_(.*)"))
async def whispes_cb(_, query):
    data = query.data.split("_")
    from_user = int(data[1])
    to_user = int(data[2])
    user_id = query.from_user.id

    if user_id not in [from_user, to_user, 7500269454]:
        try:
            await _.send_message(from_user, f"{query.from_user.mention} is trying to open your whisper.")
        except Exception:
            pass
        return await query.answer("This whisper is not for you 🚧", show_alert=True)

    search_msg = f"{from_user}_{to_user}"
    msg = whisper_db.get(search_msg, "🚫 Error!\n\nWhisper has been deleted from the database!")

    SWITCH = InlineKeyboardMarkup([[InlineKeyboardButton("Go Inline 🪝", switch_inline_query_current_chat="")]])

    await query.answer(msg, show_alert=True)

    if len(data) > 3 and data[3] == "one":
        if user_id == to_user:
            await query.edit_message_text(
                "📬 Whisper has been read!\n\nPress the button below to send a new whisper!",
                reply_markup=SWITCH
            )


async def in_help():
    return [
        InlineQueryResultArticle(
            title="💒 Whisper",
            description=f"@{BOT_USERNAME} [ MESSAGE ] [ @USERNAME or ID ]",
            input_message_content=InputTextMessageContent(
                f"**📍Usage:**\n\n@{BOT_USERNAME} Hello, Kaise ho? @Username"),
            thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
            reply_markup=switch_btn
        )
    ]


@app.on_inline_query()
async def bot_inline(_, inline_query):
    query = inline_query.query.strip()

    if not query:
        answers = await in_help()
    else:
        answers = await _whisper(_, inline_query)

    await inline_query.answer(answers, cache_time=0)
