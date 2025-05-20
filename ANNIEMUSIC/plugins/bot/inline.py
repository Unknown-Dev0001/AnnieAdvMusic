from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultPhoto,
)
from youtubesearchpython.__future__ import VideosSearch

from ANNIEMUSIC import app
from config import BANNED_USERS, BOT_USERNAME
from ANNIEMUSIC.plugins.tools.whisper import _whisper, in_help
from ANNIEMUSIC.utils.inlinequery import answer as command_articles


@app.on_inline_query(~BANNED_USERS)
async def inline_query_handler(client, inline_query):
    text = inline_query.query.strip()

    if not text:
        try:
            answers = await in_help()
            await inline_query.answer(answers, cache_time=0)
        except:
            return

    # Whisper syntax check
    elif text.lower().startswith(f"@{BOT_USERNAME.lower()}"):
        try:
            results = await _whisper(client, inline_query)
            await inline_query.answer(results, cache_time=0)
        except:
            return

    else:
        try:
            yt_search = VideosSearch(text, limit=20)
            results = (await yt_search.next()).get("result", [])
            answers = []

            for x in range(min(15, len(results))):
                title = (results[x]["title"]).title()
                duration = results[x].get("duration", "N/A")
                views = results[x].get("viewCount", {}).get("short", "N/A")
                thumbnail = results[x]["thumbnails"][0]["url"].split("?")[0]
                channellink = results[x]["channel"]["link"]
                channel = results[x]["channel"]["name"]
                link = results[x]["link"]
                published = results[x].get("publishedTime", "N/A")
                description = f"{views} | {duration} ᴍɪɴᴜᴛᴇs | {channel}  | {published}"
                buttons = InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="ʏᴏᴜᴛᴜʙᴇ 🎄", url=link)]]
                )
                searched_text = f"""
❄ <b>ᴛɪᴛʟᴇ :</b> <a href={link}>{title}</a>

⏳ <b>ᴅᴜʀᴀᴛɪᴏɴ :</b> {duration} ᴍɪɴᴜᴛᴇs
👀 <b>ᴠɪᴇᴡs :</b> <code>{views}</code>
🎥 <b>ᴄʜᴀɴɴᴇʟ :</b> <a href={channellink}>{channel}</a>
⏰ <b>ᴘᴜʙʟɪsʜᴇᴅ ᴏɴ :</b> {published}

<u><b>➻ ɪɴʟɪɴᴇ sᴇᴀʀᴄʜ ᴍᴏᴅᴇ ʙʏ {app.name}</b></u>"""
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

            # Add command articles
            answers.extend(command_articles)

            await inline_query.answer(answers, cache_time=0)
        except:
            return
