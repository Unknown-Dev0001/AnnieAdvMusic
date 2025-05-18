import requests
from ANNIEMUSIC import app
from pyrogram import Client, filters

JOKE_API_ENDPOINT = 'http://www.official-joke-api.appspot.com/random_joke'

@app.on_message(filters.command("joke"))
async def joke(_, message):
    response = requests.get(JOKE_API_ENDPOINT)
    r = response.json()
    joke_text = r['jokeContent']
    await message.reply_text(joke_text)
