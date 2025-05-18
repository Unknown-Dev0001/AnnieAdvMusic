from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from base64 import b64decode
from inspect import getfullargspec
from io import BytesIO
import asyncio
import aiohttp
from pyrogram import filters
from ANNIEMUSIC import app

button = InlineKeyboardMarkup([[
    InlineKeyboardButton("⌯ ᴄʟᴏsᴇ ⌯", callback_data="close_data")
]])

# Helper: reply or edit depending on context
async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})

# POST request with session
async def post(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                return await resp.json()
            except Exception:
                return await resp.text()

# Screenshot logic
async def take_screenshot(url: str, full: bool = False):
    url = "https://" + url if not url.startswith("http") else url
    payload = {
        "url": url,
        "width": 1100,
        "height": 1900,
        "scale": 1,
        "format": "jpeg",
    }
    if full:
        payload["full"] = True

    data = await post("https://webscreenshot.vercel.app/api", data=payload)

    if "image" not in data:
        return None

    b = data["image"].replace("data:image/jpeg;base64,", "")
    file = BytesIO(b64decode(b))
    file.name = "webss.jpg"
    return file

# Command Handler
@app.on_message(filters.command(["webss", "ss", "webshot"]))
async def take_ss(_, message: Message):
    if len(message.command) < 2:
        return await eor(message, text="**ɢɪᴠᴇ ᴀ ᴜʀʟ ᴛᴏ ғᴇᴛᴄʜ sᴄʀᴇᴇɴsʜᴏᴛ.**")

    parts = message.text.split(None, 2)
    url = parts[1]
    full = len(parts) == 3 and parts[2].lower().strip() in ["yes", "y", "1", "true"]

    m = await eor(message, text="**ᴄᴀᴘᴛᴜʀɪɴɢ sᴄʀᴇᴇɴsʜᴏᴛ...**")

    try:
        photo = await take_screenshot(url, full)
        if not photo:
            return await m.edit("**ғᴀɪʟᴇᴅ ᴛᴏ ᴛᴀᴋᴇ sᴄʀᴇᴇɴsʜᴏᴛ.**")

        await m.edit("**ᴜᴘʟᴏᴀᴅɪɴɢ...**")
        await message.reply_photo(photo, reply_markup=button)
        await m.delete()
    except Exception as e:
        await m.edit(f"**Error:** `{str(e)}`")
