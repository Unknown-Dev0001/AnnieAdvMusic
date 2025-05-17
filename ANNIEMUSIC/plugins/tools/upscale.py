import os
import aiohttp
import aiofiles
from urllib.parse import quote_plus

from ANNIEMUSIC import app
from config import PIXELCUT_API_KEY  # Ensure your key is set like: PIXELCUT_API_KEY = "sk_..."

from pyrogram import filters
from pyrogram.types import Message


async def download_from_url(path: str, url: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(path, mode="wb") as f:
                    await f.write(await resp.read())
                return path
    return None


async def post_file(url: str, file_path: str, headers: dict):
    async with aiohttp.ClientSession() as session:
        with open(file_path, 'rb') as f:
            form = aiohttp.FormData()
            form.add_field('image_file', f, filename=os.path.basename(file_path), content_type='image/jpeg')

            async with session.post(url, data=form, headers=headers) as resp:
                return await resp.json()


@app.on_message(filters.command("upscale"))
async def upscale_image(_, message: Message):
    if not PIXELCUT_API_KEY:
        return await message.reply_text("🚫 Missing Pixelcut API key.")

    reply = message.reply_to_message
    if not reply or not reply.photo:
        return await message.reply_text("📎 Please reply to an image.")

    status = await message.reply_text("🔄 Upscaling image...")

    try:
        local_path = await reply.download()
        resp = await post_file(
            "https://api.developer.pixelcut.ai/v1/upscale",
            local_path,
            headers={'Authorization': PIXELCUT_API_KEY}
        )

        image_url = resp.get("output_url") or resp.get("image") or resp.get("image_url")
        if not image_url:
            return await status.edit("❌ Upscale request failed.")

        final_path = await download_from_url(local_path, image_url)
        if not final_path:
            return await status.edit("❌ Could not download result.")

        await status.delete()
        await message.reply_document(final_path)

    except Exception as e:
        await status.edit(f"⚠️ Error: `{str(e)}`")


@app.on_message(filters.command("getdraw"))
async def draw_image(_, message: Message):
    reply = message.reply_to_message
    query = None

    if reply and reply.text:
        query = reply.text
    elif len(message.command) > 1:
        query = message.text.split(None, 1)[1]

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
            return await status.edit("❌ Error downloading image.")

        await status.delete()
        await message.reply_photo(final_path, caption=f"`{query}`")

    except Exception as e:
        await status.edit(f"⚠️ Error: `{str(e)}`")
