from pyrogram import filters
from pyrogram.types import Message
from datetime import datetime

from ANNIEMUSIC import app, SUDOERS, LOGGER
from ANNIEMUSIC.misc import SUDOERS as SUDO_USERS
from ANNIEMUSIC.utils.database import add_gban_user, remove_gban_user
from ANNIEMUSIC.utils.decorators.language import language
from ANNIEMUSIC.utils.extraction import extract_user
from config import BANNED_USERS, OWNER_ID, LOGGER_ID


@app.on_message(filters.command(["block"]) & SUDOERS)
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text(_["general_1"])

    user = await extract_user(message)

    # Protect OWNER_ID
    if user.id == OWNER_ID:
        await message.reply_text("You can't block my master, let me block you 🤣")
        await add_gban_user(message.from_user.id)
        BANNED_USERS.add(message.from_user.id)
        if message.from_user.id in SUDO_USERS:
            SUDO_USERS.remove(message.from_user.id)
        await message.reply_text("Done ✅\nAab nikal yaha se😐")

        # Log this attempt
        try:
            from_user = message.from_user
            name = from_user.first_name + (f" {from_user.last_name}" if from_user.last_name else "")
            username = f"@{from_user.username}" if from_user.username else "No username"
            user_id = from_user.id
            profile_link = f"https://t.me/{from_user.username}" if from_user.username else f"tg://user?id={from_user.id}"
            time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            await app.send_message(
                LOGGER_ID,
                f"⚠️ **Unauthorized Block Attempt**\n\n"
                f"**Name:** {name}\n"
                f"**Username:** {username}\n"
                f"**User ID:** `{user_id}`\n"
                f"**Profile:** [Click Here]({profile_link})\n"
                f"**Time:** `{time}`\n\n"
                f"Action Taken: Blocked and removed from SUDO for attempting to block the OWNER."
            )
        except Exception as e:
            await LOGGER(__name__).error(f"Failed to log to LOGGER_ID: {e}")
        return

    if user.id in BANNED_USERS:
        return await message.reply_text(_["block_1"].format(user.mention))
    await add_gban_user(user.id)
    BANNED_USERS.add(user.id)
    await message.reply_text(_["block_2"].format(user.mention))


@app.on_message(filters.command(["unblock"]) & SUDOERS)
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id not in BANNED_USERS:
        return await message.reply_text(_["block_3"].format(user.mention))
    await remove_gban_user(user.id)
    BANNED_USERS.remove(user.id)
    await message.reply_text(_["block_4"].format(user.mention))


@app.on_message(filters.command(["blocked", "blockedusers", "blusers"]) & SUDOERS)
@language
async def sudoers_list(client, message: Message, _):
    if not BANNED_USERS:
        return await message.reply_text(_["block_5"])
    mystic = await message.reply_text(_["block_6"])
    msg = _["block_7"]
    count = 0
    for users in BANNED_USERS:
        try:
            user = await app.get_users(users)
            user = user.first_name if not user.mention else user.mention
            count += 1
            msg += f"{count}➤ {user}\n"
        except:
            continue
    return await mystic.edit_text(msg if count else _["block_5"])
