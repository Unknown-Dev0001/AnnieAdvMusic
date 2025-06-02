import requests
from ANNIEMUSIC import app
from pyrogram import filters


@app.on_message(filters.command("fakeinfo"))
async def address(_, message):
    # Get the nationality code safely
    try:
        query = message.text.split(maxsplit=1)[1].strip().lower()
    except IndexError:
        query = "us"  # default nationality

    url = f"https://randomuser.me/api/?nat={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        await message.reply_text(f"API error: {e}")
        return

    if "results" not in data or not data["results"]:
        await message.reply_text("❌ No user data found.")
        return

    try:
        user_data = data["results"][0]

        name = f"{user_data['name']['title']} {user_data['name']['first']} {user_data['name']['last']}"
        address = f"{user_data['location']['street']['number']} {user_data['location']['street']['name']}" 
        city = user_data['location']['city']
        state = user_data['location']['state']
        country = user_data['location']['country'] 
        postal = user_data['location']['postcode']
        email = user_data['email']
        phone = user_data['phone']
        picture_url = user_data['picture']['large']

        caption = f"""
﹝⌬﹞**ɴᴀᴍᴇ** ⇢ {name}
﹝⌬﹞**ᴀᴅᴅʀᴇss** ⇢ {address}
﹝⌬﹞**ᴄᴏᴜɴᴛʀʏ** ⇢ {country}
﹝⌬﹞**ᴄɪᴛʏ** ⇢ {city}
﹝⌬﹞**sᴛᴀᴛᴇ** ⇢ {state}
﹝⌬﹞**ᴘᴏsᴛᴀʟ** ⇢ {postal}
﹝⌬﹞**ᴇᴍᴀɪʟ** ⇢ {email}
﹝⌬﹞**ᴘʜᴏɴᴇ** ⇢ {phone}
        """

        await message.reply_photo(photo=picture_url, caption=caption)
    except Exception as e:
        await message.reply_text(f"❌ Failed to parse user data: {e}")
