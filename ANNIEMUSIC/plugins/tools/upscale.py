import os
import aiohttp
import aiofiles
from urllib.parse import quote_plus

from pyrogram import Client, filters
from pyrogram.types import Message
from ANNIEMUSIC import app


# === Helper: Download File from URL ===
async def download_from_url(path: str, url: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(path, mode="wb") as f:
                    await f.write(await resp.read())
                return path
    return None


# === /upscale ===
@app.on_message(filters.command("upscale"))
async def upscale_image(client: Client, message: Message):
    replied = message.reply_to_message
    if not replied or not replied.photo:
        return await message.reply_text("❗ Please reply to an image.")

    status = await message.reply_text("🔄 Upscaling image...")

    try:
        # Get file info
        file_info = await client.get_file(replied.photo.file_id)
        file_url = f"https://api.telegram.org/file/bot{client.token}/{file_info.file_path}"

        # API URL
        upscale_api = f"https://enhance.itz-ashlynn.workers.dev/?url={file_url}"

        # Download the result
        output_path = f"cache/upscaled_{message.id}.jpg"
        result = await download_from_url(output_path, upscale_api)

        if not result:
            return await status.edit("❌ Upscaling failed.")

        await status.delete()
        await message.reply_document(result)

    except Exception as e:
        await status.edit(f"⚠️ Error: `{str(e)}`")


# === /gen ===
@app.on_message(filters.command("gen"))
async def draw_image(_, message: Message):
    reply = message.reply_to_message
    query = reply.text if reply and reply.text else message.text.split(None, 1)[1] if len(message.command) > 1 else None

    if not query:
        return await message.reply_text("💬 Please reply or provide text.")

    status = await message.reply_text("🎨 Generating image...")

    try:
        safe_prompt = quote_plus(query)
        image_url = f"https://botfather.cloud/Apis/ImgGen/client.php?inputText={safe_prompt}"

        user_id = message.from_user.id
        chat_id = message.chat.id
        temp_path = f"cache/{user_id}_{chat_id}_{message.id}.jpg"

        final_path = await download_from_url(temp_path, image_url)
        if not final_path:
            return await status.edit("❌ Failed to download image.")

        await status.delete()
        await message.reply_photo(final_path, caption=f"`{query}`")
    except Exception as e:
        await status.edit(f"⚠️ Error: `{str(e)}`")
