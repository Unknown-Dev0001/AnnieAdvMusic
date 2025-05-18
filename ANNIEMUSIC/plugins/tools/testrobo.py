from telethon import TelegramClient, events
from telethon.tl.functions.channels import LeaveChannelRequest
import asyncio
from config import API_ID, API_HASH, BOT_TOKEN, AUTHORIZED_USERS

bot = TelegramClient("kick_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern="/kickall"))
async def kick_all_members(event):
    if event.sender_id not in AUTHORIZED_USERS:
        return await event.reply("You are not authorized to use this command.")

    if not event.is_group:
        return await event.reply("This command can only be used in groups.")

    chat = await event.get_chat()
    me = await bot.get_me()
    count = 0

    await event.reply("Kicking all non-admin members...")

    async for member in bot.iter_participants(chat):
        try:
            if member.id == me.id:
                continue  # skip self
            permissions = await bot.get_permissions(chat.id, member.id)
            if permissions.is_admin:
                continue  # skip admins
            await bot.kick_participant(chat.id, member.id)
            count += 1
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Failed to kick {member.id}: {e}")

    await event.reply(f"✅ Kicked {count} members.\nNow leaving the group...")
    await bot(LeaveChannelRequest(chat.id))

print("🤖 Bot is running...")
bot.run_until_disconnected()
