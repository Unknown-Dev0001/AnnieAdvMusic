import os
import aiohttp
import aiofiles
import requests
from urllib.parse import quote_plus

from pyrogram import Client, filters
from pyrogram.types import Message
from ANNIEMUSIC import app
from config import BOT_USERNAME


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
@app.on_message(filters.command("upscale", prefixes="/"))
async def upscale_image(client, message: Message):
    replied = message.reply_to_message
    if not replied or not replied.photo:
        return await message.reply_text("❗ Please reply to an image.")

    status = await message.reply_text("🔄 Upscaling image...")

    try:
        image = await replied.download()
        response = requests.post(
            "https://api.deepai.org/api/torch-srgan",
            files={'image': open(image, 'rb')},
            headers={'api-key': 'bf9ee957-9fad-46f5-a403-3e96ca9004e4'}
        )
        response.raise_for_status()
        data = response.json()
        output_url = data.get("output_url")

        if not output_url:
            return await status.edit("❌ Upscale failed: No output received.")

        output_path = await download_from_url(image, output_url)
        await status.delete()
        await message.reply_document(output_path)

    except requests.exceptions.RequestException as e:
        await status.edit(f"❌ Request error: {str(e)}")
    except Exception as e:
        await status.edit(f"⚠️ Unexpected error: {str(e)}")


# === /waifu ===
waifu_api_url = 'https://api.waifu.im/search'


def get_waifu_data(tags):
    params = {
        'included_tags': tags,
        'height': '>=2000'
    }
    response = requests.get(waifu_api_url, params=params)
    if response.status_code == 200:
        return response.json()
    return None


@app.on_message(filters.command("waifu"))
def waifu_command(client, message: Message):
    try:
        tags = ['maid']
        waifu_data = get_waifu_data(tags)

        if waifu_data and 'images' in waifu_data:
            first_image = waifu_data['images'][0]
            image_url = first_image['url']
            message.reply_photo(image_url)
        else:
            message.reply_text("❌ No waifu found with the specified tags.")
    except Exception as e:
        message.reply_text(f"⚠️ Error: {str(e)}")


# === /getdraw ===
@app.on_message(filters.command("getdraw"))
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
