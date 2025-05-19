from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultPhoto,
)
from youtubesearchpython.__future__ import VideosSearch
from ANNIEMUSIC import app
from config import BANNED_USERS, BOT_USERNAME
from ANNIEMUSIC.plugins.tools.whisper import _whisper, in_help
import re


def is_whisper_query(text: str) -> bool:
    # Check for: @BotUsername some message @username or user_id
    pattern = fr"@{BOT_USERNAME.lower()}\s.+\s(@[\w\d_]+|\d+)$"
    return re.match(pattern, text.strip().lower()) is not None


@app.on_inline_query(~BANNED_USERS)
async def inline_query_handler(client, inline_query):
    text = inline_query.query.strip()

    if text == "":
        try:
            answers = await in_help()
            return await inline_query.answer(answers, cache_time=0)
        except Exception:
            return

    elif is_whisper_query(text):
        try:
            results = await _whisper(client, inline_query)
            return await inline_query.answer(results, cache_time=0)
        except Exception:
            return

    else:
        try:
            a = VideosSearch(text, limit=20)
            result = (await a.next()).get("result", [])
            answers = []
            for x in range(min(15, len(result))):
                video = result[x]
                title = video["title"]
                duration = video.get("duration", "N/A")
                views = video.get("viewCount", {}).get("short", "N/A")
                thumbnail = video["thumbnails"][0]["url"].split("?")[0]
                channellink = video["channel"]["link"]
                channel = video["channel"]["name"]
                link = video["link"]
                published = video.get("publishedTime", "N/A")
                description = f"{views} | {duration} ᴍɪɴᴜᴛᴇs | {channel} | {published}"
                buttons = InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="ʏᴏᴜᴛᴜʙᴇ 🎄", url=link)]]
                )
                searched_text = f"""
❄ <b>ᴛɪᴛʟᴇ :</b> <a href="{link}">{title}</a>

⏳ <b>ᴅᴜʀᴀᴛɪᴏɴ :</b> {duration} ᴍɪɴᴜᴛᴇs
👀 <b>ᴠɪᴇᴡs :</b> <code>{views}</code>
🎥 <b>ᴄʜᴀɴɴᴇʟ :</b> <a href="{channellink}">{channel}</a>
⏰ <b>ᴘᴜʙʟɪꜱʜᴇᴅ ᴏɴ :</b> {published}

<u><b>➻ ɪɴʟɪɴᴇ ꜱᴇᴀʀᴄʜ ᴍᴏᴅᴇ ʙʏ {app.name}</b></u>"""
                answers.append(
                    InlineQueryResultPhoto(
                        photo_url=thumbnail,
                        title=title,
                        thumb_url=thumbnail,
                        description=description,
                        caption=searched_text,
                        reply_markup=buttons,
                    )
                )
            return await inline_query.answer(answers)
        except Exception:
            return
