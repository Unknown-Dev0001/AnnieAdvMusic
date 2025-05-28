from ANNIEMUSIC import app
import requests as r
from pyrogram import filters
from pyrogram.types import Message
import asyncio

# AI Assistant API URL
API_URL = "https://api-aiassistant.eternalowner06.workers.dev/"

@app.on_message(filters.command(["bingsearch", "bing", "search"]))
async def ai_text_response(client, message: Message):
    try:
        if len(message.command) == 1:
            await message.reply_text("❗ Please provide a prompt.\n\nExample:\n`/bingsearch What is NDA exam?`")
            return

        prompt = " ".join(message.command[1:])

        # Step 1: Loading...
        loading_msg = await message.reply_text("🔄 Loading...")

        # Step 2: Please Wait...
        await asyncio.sleep(1.2)
        await loading_msg.edit_text("⏳ Please wait...")

        # Step 3: Almost Done...
        await asyncio.sleep(1.2)
        await loading_msg.edit_text("✅ Almost done...")

        # Fetch AI response
        response = r.get(f"{API_URL}?prompt={prompt}")

        if response.status_code == 200:
            data = response.json()
            try:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                await loading_msg.edit_text(text.strip())
            except (KeyError, IndexError):
                await loading_msg.edit_text("⚠️ Unexpected response format from AI.")
        else:
            await loading_msg.edit_text("❌ Failed to get response from AI. Try again later.")

    except Exception as e:
        await loading_msg.edit_text(f"⚠️ An error occurred:\n`{str(e)}`")
