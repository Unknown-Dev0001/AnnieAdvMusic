import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from ANNIEMUSIC import LOGGER, app, userbot
from ANNIEMUSIC.core.call import JARVIS
from ANNIEMUSIC.misc import sudo
from ANNIEMUSIC.plugins import ALL_MODULES
from ANNIEMUSIC.utils.database import get_banned_users, get_gbanned
from ANNIEMUSIC.utils.cookie_handler import fetch_and_store_cookies
from web import start_webserver, ping_server  # Corrected import
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant session not filled. Please provide a Pyrogram session string.")
        exit()

    try:
        await fetch_and_store_cookies()
        LOGGER("ANNIEMUSIC").info("YᴏᴜTᴜʙᴇ ᴄᴏᴏᴋɪᴇs ʟᴏᴀᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.")
    except Exception as e:
        LOGGER("ANNIEMUSIC").warning(f"Cookie error: {e}")

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("ANNIEMUSIC.plugins" + all_module)

    LOGGER("ANNIEMUSIC.plugins").info("Mᴏᴅᴜʟᴇs ʟᴏᴀᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.")

    await userbot.start()
    await JARVIS.start()

    try:
        await JARVIS.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ANNIEMUSIC").error(
            "Vᴏɪᴄᴇ ᴄʜᴀᴛ ɴᴏᴛ ᴇɴᴀʙʟᴇᴅ ɪɴ ᴛʜᴇ ʟᴏɢ ɢʀᴏᴜᴘ. Sᴛᴏᴘᴘɪɴɢ Bᴏᴛ..."
        )
        exit()
    except:
        pass

    await JARVIS.decorators()

    if config.WEB_SERVER:
        asyncio.create_task(start_webserver())
        asyncio.create_task(ping_server(config.PING_URL, config.PING_TIME))

    LOGGER("ANNIEMUSIC").info("Mᴜsɪᴄ ʙᴏᴛ Sᴛᴀʀᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ. Dᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ Sʜɪᴠᴀᴍ Yᴀᴅᴀᴠ 😎")
    await idle()

    await app.stop()
    await userbot.stop()
    LOGGER("ANNIEMUSIC").info("Sᴛᴏᴘᴘɪɴɢ Mᴜsɪᴄ Bᴏᴛ...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
