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

# Screenshot logic with Abstract API
async def take_screenshot(url: str):
    url = "https://" + url if not url.startswith("http") else url
    full_url = f"https://screenshot.abstractapi.com/v1/?api_key=bec04934e07441bb86504e1149a88232&url={url}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(full_url) as resp:
            if resp.status != 200:
                return None
            image = await resp.read()

    file = BytesIO(image)
    file.name = "webss.jpg"
    return file

# Command Handler
@app.on_message(filters.command(["webss", "ss", "web"]))
async def take_ss(_, message: Message):
    if len(message.command) < 2:
        return await eor(message, text="**ɢɪᴠᴇ ᴀ ᴜʀʟ ᴛᴏ ғᴇᴛᴄʜ sᴄʀᴇᴇɴsʜᴏᴛ.**")

    url = message.text.split(None, 1)[1]

    m = await eor(message, text="**ᴄᴀᴘᴛᴜʀɪɴɢ sᴄʀᴇᴇɴsʜᴏᴛ...**")

    try:
        photo = await take_screenshot(url)
        if not photo:
            return await m.edit("**ғᴀɪʟᴇᴅ ᴛᴏ ᴛᴀᴋᴇ sᴄʀᴇᴇɴsʜᴏᴛ.**")

        await m.edit("**ᴜᴘʟᴏᴀᴅɪɴɢ...**")
        await message.reply_photo(photo, reply_markup=button)
        await m.delete()
    except Exception as e:
        await m.edit(f"**Error:** `{str(e)}`")
