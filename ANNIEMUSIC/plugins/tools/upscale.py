import os
import aiohttp
import aiofiles
import asyncio
from urllib.parse import quote_plus

from pyrogram import Client, filters
from pyrogram.types import Message
from ANNIEMUSIC import app

# === Config ===
CACHE_FOLDER = "cache"
UPSCALE_API_URL = "https://bj-devs.serv00.net/ImagesEnhance.php?imageurl="
GEN_API_URL = "https://botfather.cloud/Apis/ImgGen/client.php?inputText="
API_TIMEOUT = 20  # seconds
MAX_RETRIES = 2


# === Helper: Download File from URL ===
async def download_from_url(path: str, url: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(path, mode="wb") as f:
                        await f.write(await resp.read())
                    return path
    except Exception:
        pass
    return None


# === Helper: Cleanup old files ===
async def cleanup_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


# === Helper: Animate status message ===
async def animate_status(message: Message, text: str, stop_event: asyncio.Event, frames: list):
    i = 0
    while not stop_event.is_set():
        frame = frames[i % len(frames)]
        try:
            await message.edit_text(f"{frame} {text}")
        except Exception:
            pass
        i += 1
        await asyncio.sleep(0.7)


# === /upscale ===
@app.on_message(filters.command("upscale"))
async def upscale_image(client: Client, message: Message):
    replied = message.reply_to_message
    if not replied or not replied.photo:
        return await message.reply_text("❗ Please reply to an image.")

    status = await message.reply_text("🔄 Upscaling image...")
    upscale_frames = ["🖼️", "✨", "🔍", "🛠️", "🔄"]

    stop_event = asyncio.Event()
    animation_task = asyncio.create_task(animate_status(status, "Upscaling image...", stop_event, upscale_frames))

    try:
        # Get file info
        file_info = await client.get_file(replied.photo.file_id)
        file_url = f"https://api.telegram.org/file/bot{client.token}/{file_info.file_path}"
        safe_url = quote_plus(file_url)

        # Retry loop
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)) as session:
                    async with session.get(f"{UPSCALE_API_URL}{safe_url}") as resp:
                        if resp.status != 200:
                            raise Exception("Failed to contact upscale API.")

                        data = await resp.json()
                        if data.get("status") != "success" or "download_url" not in data:
                            raise Exception("API returned error or missing download URL.")

                        download_url = data["download_url"]

                # Download the result
                output_path = f"{CACHE_FOLDER}/upscaled_{message.id}.jpg"
                result = await download_from_url(output_path, download_url)

                if not result:
                    raise Exception("Failed to download upscaled image.")

                stop_event.set()
                await animation_task
                await status.delete()
                await message.reply_document(result, caption="🔍 Upscaled Image")
                await cleanup_file(output_path)
                return

            except Exception as e:
                if attempt == MAX_RETRIES:
                    stop_event.set()
                    await animation_task
                    return await status.edit(f"❌ Upscaling failed. Error: `{str(e)}`")
                await asyncio.sleep(2)

    except Exception as e:
        stop_event.set()
        await animation_task
        await status.edit(f"⚠️ Unexpected error: `{str(e)}`")


# === /gen ===
@app.on_message(filters.command("gen"))
async def draw_image(_, message: Message):
    reply = message.reply_to_message
    query = reply.text if reply and reply.text else message.text.split(None, 1)[1] if len(message.command) > 1 else None

    if not query:
        return await message.reply_text("💬 Please reply or provide text.")

    status = await message.reply_text("🎨 Generating image...")
    gen_frames = ["🖌️", "🎨", "🖍️", "🖼️", "✨"]

    stop_event = asyncio.Event()
    animation_task = asyncio.create_task(animate_status(status, "Generating image...", stop_event, gen_frames))

    try:
        safe_prompt = quote_plus(query)
        image_url = f"{GEN_API_URL}{safe_prompt}"

        user_id = message.from_user.id
        chat_id = message.chat.id
        temp_path = f"{CACHE_FOLDER}/{user_id}_{chat_id}_{message.id}.jpg"

        result = await download_from_url(temp_path, image_url)
        if not result:
            stop_event.set()
            await animation_task
            return await status.edit("❌ Failed to download generated image.")

        stop_event.set()
        await animation_task
        await status.delete()
        await message.reply_photo(result, caption=f"`{query}`")
        await cleanup_file(temp_path)

    except Exception as e:
        stop_event.set()
        await animation_task
        await status.edit(f"⚠️ Error: `{str(e)}`")


# === /clearcache ===
@app.on_message(filters.command("clearcache"))
async def clear_cache(_, message: Message):
    try:
        files_deleted = 0
        if os.path.exists(CACHE_FOLDER):
            for filename in os.listdir(CACHE_FOLDER):
                file_path = os.path.join(CACHE_FOLDER, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        files_deleted += 1
                except Exception:
                    pass

        await message.reply_text(f"🗑️ Cache cleared! Files deleted: `{files_deleted}`")

    except Exception as e:
        await message.reply_text(f"⚠️ Error clearing cache: `{str(e)}`")
