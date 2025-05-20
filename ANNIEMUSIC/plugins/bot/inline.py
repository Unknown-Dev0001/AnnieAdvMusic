from ANNIEMUSIC.utils.inlinequery import answer as cmd_answer  
from ANNIEMUSIC.plugins.tools.whisper import _whisper
from pyrogram.types import (
    InlineQueryResultPhoto, InlineKeyboardMarkup, InlineKeyboardButton
)
from youtubesearchpython import VideosSearch
from ANNIEMUSIC import app
from config import BANNED_USERS

@app.on_inline_query(~BANNED_USERS)
async def inline_query_handler(client, inline_query):
    query = inline_query.query.strip()

    if not query:
        # Show CMD command buttons when query is empty
        await inline_query.answer(cmd_answer, cache_time=0)
        return

    # Check for whisper syntax (last word is @username or digit ID)
    parts = query.split()
    if len(parts) >= 2:
        last = parts[-1]
        if last.startswith("@") or last.isdigit():
            try:
                results = await _whisper(client, inline_query)
                return await inline_query.answer(results, cache_time=0)
            except Exception:
                pass

    # Else perform YouTube search for everything else
    try:
        a = VideosSearch(query, limit=20)
        result = (await a.next()).get("result", [])
        answers = []
        for x in range(min(15, len(result))):
            title = result[x]["title"].title()
            duration = result[x].get("duration", "N/A")
            views = result[x].get("viewCount", {}).get("short", "N/A")
            thumbnail = result[x]["thumbnails"][0]["url"].split("?")[0]
            channellink = result[x]["channel"]["link"]
            channel = result[x]["channel"]["name"]
            link = result[x]["link"]
            published = result[x].get("publishedTime", "N/A")
            description = f"{views} | {duration} ᴍɪɴ | {channel} | {published}"
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("ʏᴏᴜᴛᴜʙᴇ 🎄", url=link)]
            ])
            searched_text = f"""
❄ <b>ᴛɪᴛʟᴇ :</b> <a href={link}>{title}</a>

⏳ <b>ᴅᴜʀᴀᴛɪᴏɴ :</b> {duration} ᴍɪɴᴜᴛᴇs
👀 <b>ᴠɪᴇᴡs :</b> <code>{views}</code>
🎥 <b>ᴄʜᴀɴɴᴇʟ :</b> <a href={channellink}>{channel}</a>
⏰ <b>ᴘᴜʙʟɪsʜᴇᴅ :</b> {published}

<u><b>➻ ɪɴʟɪɴᴇ ʙʏ {app.name}</b></u>
"""
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
        await inline_query.answer(answers)
    except Exception:
        pass
