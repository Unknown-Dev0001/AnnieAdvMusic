import requests
import asyncio
from ANNIEMUSIC import app
from pyrogram import filters

JOKE_API_ENDPOINT = 'https://official-joke-api.appspot.com/random_joke'

@app.on_message(filters.command("joke"))
async def joke(_, message):
    response = requests.get(JOKE_API_ENDPOINT)
    if response.status_code == 200:
        r = response.json()
        setup_msg = await message.reply_text(f"**{r['setup']}**\n\n_Think about it...🤔_")
        await asyncio.sleep(3)  # suspense delay
        await setup_msg.edit_text(f"**{r['setup']}**\n\n**{r['punchline']}**")
    else:
        await message.reply_text("Couldn't fetch a joke at the moment. Try again later! 😢")
