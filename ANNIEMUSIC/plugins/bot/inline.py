import re
import traceback
from pyrogram import Client
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultPhoto,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from youtubesearchpython.__future__ import VideosSearch
from ANNIEMUSIC import app
from config import BANNED_USERS
from ANNIEMUSIC.utils.inlinequery import answer as cmd_answer
from ANNIEMUSIC.plugins.tools.whisper import _whisper

# Set True for debug logs (set to False in production)
DEBUG = True

# Regex pattern for whisper syntax
whisper_syntax = re.compile(r".+ [@]?\w+$")

@app.on_inline_query(~BANNED_USERS)
async def inline_query_handler(client: Client, inline_query: InlineQuery):
    query = inline_query.query.strip()

    if DEBUG:
        print("Inline query received:", query)

    # Case 1: Empty query → show CMD command buttons
    if not query:
        if DEBUG:
            print("Empty query — sending cmd_answer")
        await inline_query.answer(cmd_answer, cache_time=0)
        return

    # Case 2: Whisper query → use _whisper plugin
    if len(query.split()) >= 2 and whisper_syntax.match(query):
        try:
            if DEBUG:
                print("Whisper pattern matched — processing via _whisper")
            results = await _whisper(client, inline_query)
            await inline_query.answer(results, cache_time=0)
            return
        except Exception:
            if DEBUG:
                print("Error in _whisper — falling back to cmd_answer")
            await inline_query.answer(cmd_answer, cache_time=0)
            return

    # Case 3: YouTube Search
    try:
        if DEBUG:
            print("Performing YouTube search...")
        search = VideosSearch(query, limit=20)
        results = (await search.next()).get("result", [])

        if DEBUG:
            print(f"Found {len(results)} results.")

        if not results:
            if DEBUG:
                print("No results found for YouTube query.")
            await inline_query.answer([
                InlineQueryResultArticle(
                    title="No results found",
                    input_message_content=InputTextMessageContent(
                        f"No YouTube videos found for: <code>{query}</code>"
                    )
                )
            ])
            return

        answers = []
        for item in results[:15]:
            title = item["title"].title()
            duration = item.get("duration", "N/A")
            views = item.get("viewCount", {}).get("short", "N/A")
            thumbnail = item["thumbnails"][0]["url"].split("?")[0]
            channellink = item["channel"]["link"]
            channel = item["channel"]["name"]
            link = item["link"]
            published = item.get("publishedTime", "N/A")
            description = f"{views} | {duration} ᴍɪɴ | {channel} | {published}"

            if DEBUG:
                print("Thumbnail URL:", thumbnail)

            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("ʏᴏᴜᴛᴜʙᴇ 🎄", url=link)]
            ])

            searched_text = f"""
❄ <b>ᴛɪᴛʟᴇ :</b> <a href="{link}">{title}</a>

⏳ <b>ᴅᴜʀᴀᴛɪᴏɴ :</b> {duration} ᴍɪɴᴜᴛᴇs
👀 <b>ᴠɪᴇᴡs :</b> <code>{views}</code>
🎥 <b>ᴄʜᴀɴɴᴇʟ :</b> <a href="{channellink}">{channel}</a>
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
        if DEBUG:
            print("Error in YouTube search block:")
            print(traceback.format_exc())
        await inline_query.answer(cmd_answer, cache_time=0)
