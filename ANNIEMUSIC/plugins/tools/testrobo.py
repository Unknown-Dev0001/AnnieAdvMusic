from telethon import TelegramClient, events
from telethon.tl.functions.channels import LeaveChannelRequest
import asyncio
from config import API_ID, API_HASH, BOT_TOKEN, AUTHORIZED_USERS

bot = TelegramClient("kick_bot", API_ID, API_HASH)

@bot.on(events.NewMessage(pattern="/quiz"))
async def kick_all_members(event):
    if event.sender_id not in AUTHORIZED_USERS:
        return await event.reply("You are not authorized.")
    chat = await event.get_chat()

    # Allow only groups and supergroups (megagroup=True)
    if not getattr(chat, "megagroup", False):
        return await event.reply("This command works only in groups.")

    me = await bot.get_me()
    count = 0
    await event.reply("Starting to kick all non-admin members...")

    async for member in bot.iter_participants(chat):
        try:
            if member.id == me.id:
                continue
            perms = await bot.get_permissions(chat.id, member.id)
            if perms.admin_rights or perms.creator:
                continue
            await bot.edit_permissions(chat.id, member.id, view_messages=False)
            count += 1
            await asyncio.sleep(1)  # Delay to avoid flood limits
        except Exception as e:
            print(f"Error kicking {member.id}: {e}")

    await event.reply(f"Kicked {count} members. Leaving group now.")
    await bot(LeaveChannelRequest(chat.id))

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot is running...")
    await bot.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
