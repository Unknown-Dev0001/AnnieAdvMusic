from ANNIEMUSIC import app
from config import BOT_USERNAME
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

whisper_db = {}

switch_btn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("💒 Start Whisper", switch_inline_query_current_chat="")]]
)

async def _whisper(_, inline_query):
    data = inline_query.query.strip()
    results = []

    # Split only once from right to get message and user_id
    parts = data.rsplit(" ", 1)
    if len(parts) != 2:
        return [
            InlineQueryResultArticle(
                title="💒 Whisper",
                description=f"@{BOT_USERNAME} [ MESSAGE ] [ @USERNAME or ID ]",
                input_message_content=InputTextMessageContent(
                    f"💒 Usage:\n\n@{BOT_USERNAME} [ MESSAGE ] [ @USERNAME or ID ]\n\nExample:\n@{BOT_USERNAME} Hello there @someone"
                ),
                thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
                reply_markup=switch_btn,
            )
        ]

    msg, user_id = parts

    try:
        user = await _.get_users(user_id)
    except Exception:
        return [
            InlineQueryResultArticle(
                title="💒 Whisper",
                description="Invalid username or ID!",
                input_message_content=InputTextMessageContent("Invalid username or ID!"),
                thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
                reply_markup=switch_btn,
            )
        ]

    whisper_db[f"{inline_query.from_user.id}_{user.id}"] = msg

    whisper_btn = InlineKeyboardMarkup(
        [[InlineKeyboardButton("💒 Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}")]]
    )
    one_time_whisper_btn = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔩 One-Time Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}_one")]]
    )

    return [
        InlineQueryResultArticle(
            title="💒 Whisper",
            description=f"Send a Whisper to {user.first_name}!",
            input_message_content=InputTextMessageContent(
                f"💒 You've sent a whisper to {user.first_name}."
            ),
            thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
            reply_markup=whisper_btn,
        ),
        InlineQueryResultArticle(
            title="🔩 One-Time Whisper",
            description=f"Send a one-time whisper to {user.first_name}!",
            input_message_content=InputTextMessageContent(
                f"🔩 You've sent a one-time whisper to {user.first_name}."
            ),
            thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
            reply_markup=one_time_whisper_btn,
        ),
    ]


@app.on_callback_query(filters.regex(pattern=r"fdaywhisper_(.*)"))
async def whisper_callback(_, query):
    data = query.data.split("_")
    from_user = int(data[1])
    to_user = int(data[2])
    user_id = query.from_user.id

    if user_id not in [from_user, to_user, 7500269454]:  # Replace 7500269454 with your OWNER_ID
        try:
            await _.send_message(from_user, f"{query.from_user.mention} tried to open your whisper.")
        except:
            pass
        return await query.answer("This whisper is not for you!", show_alert=True)

    msg = whisper_db.get(f"{from_user}_{to_user}", "🚫 Whisper deleted from database!")

    await query.answer(msg, show_alert=True)

    if len(data) > 3 and data[3] == "one" and user_id == to_user:
        await query.edit_message_text(
            "📬 Whisper has been read!\n\nTap below to send a new one!",
            reply_markup=switch_btn,
        )


async def in_help():
    return [
        InlineQueryResultArticle(
            title="💒 Whisper",
            description=f"@{BOT_USERNAME} [ MESSAGE ] [ @USERNAME or ID ]",
            input_message_content=InputTextMessageContent(
                f"**Usage:**\n@{BOT_USERNAME} Hello @username"
            ),
            thumb_url="https://te.legra.ph/file/3eec679156a393c6a1053.jpg",
            reply_markup=switch_btn,
        )
    ]
