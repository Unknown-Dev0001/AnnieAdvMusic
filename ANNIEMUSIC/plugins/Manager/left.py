from ANNIEMUSIC import app
from pyrogram import Client
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageDraw, ImageFont
import asyncio
import os

# --------------------------------------------------------------------------------- #

def get_font(font_size, font_path):
    return ImageFont.truetype(font_path, font_size)

def resize_text(text_size, text):
    return (text[:text_size] + "...").upper() if len(text) > text_size else text.upper()

# --------------------------------------------------------------------------------- #

async def get_userinfo_img(bg_path, font_path, user_id, profile_path=None):
    try:
        bg = Image.open(bg_path)
    except Exception as e:
        print(f"Error loading background image: {e}")
        return None

    if profile_path:
        try:
            img = Image.open(profile_path)
            mask = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.pieslice([(0, 0), img.size], 0, 360, fill=255)

            circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
            circular_img.paste(img, (0, 0), mask)
            resized = circular_img.resize((400, 400))
            bg.paste(resized, (440, 160), resized)
        except Exception as e:
            print(f"Error processing profile image: {e}")
            return None

    img_draw = ImageDraw.Draw(bg)
    img_draw.text(
        (529, 627),
        text=str(user_id).upper(),
        font=get_font(46, font_path),
        fill=(255, 255, 255),
    )

    path = f"./userinfo_img_{user_id}.png"
    bg.save(path)
    return path

# --------------------------------------------------------------------------------- #

bg_path = "ANNIEMUSIC/assets/userinfo.png"
font_path = "ANNIEMUSIC/assets/hiroko.ttf"

# Check if paths exist
assert os.path.exists(bg_path), "❌ Background image not found"
assert os.path.exists(font_path), "❌ Font file not found"

# --------------------------------------------------------------------------------- #

@app.on_chat_member_updated()
async def member_has_left(client: Client, member: ChatMemberUpdated):
    # Check if user left or was removed
    if (
        member.old_chat_member
        and member.new_chat_member
        and member.old_chat_member.status in {"member", "administrator", "restricted"}
        and member.new_chat_member.status in {"left", "kicked"}
    ):
        user = member.old_chat_member.user or member.from_user

        photo_id = getattr(user.photo, "big_file_id", None)
        if not photo_id:
            print(f"User {user.id} has no profile photo.")
            return

        try:
            photo = await client.download_media(photo_id)

            welcome_photo = await get_userinfo_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user.id,
                profile_path=photo,
            )

            if not welcome_photo:
                return

            caption = (
                f"**❅─────✧❅✦❅✧─────❅**\n\n"
                f"**๏ ᴀ ᴍᴇᴍʙᴇʀ ʟᴇғᴛ ᴛʜᴇ ɢʀᴏᴜᴘ🥀**\n\n"
                f"**➻** {user.mention}\n\n"
                f"**๏ ᴏᴋ ʙʏᴇ ᴅᴇᴀʀ ᴀɴᴅ ʜᴏᴘᴇ ᴛᴏ sᴇᴇ ʏᴏᴜ ᴀɢᴀɪɴ ɪɴ ᴛʜɪs ᴄᴜᴛᴇ ɢʀᴏᴜᴘ ᴡɪᴛʜ ʏᴏᴜʀ ғʀɪᴇɴᴅs✨**\n\n"
                f"**ㅤ•─╼⃝𖠁 ʙʏᴇ ♡︎ ʙᴀʙʏ 𖠁⃝╾─•**"
            )

            button_text = "๏ ᴠɪᴇᴡ ᴜsᴇʀ ๏"
            deep_link = f"tg://openmessage?user_id={user.id}"

            msg = await client.send_photo(
                chat_id=member.chat.id,
                photo=welcome_photo,
                caption=caption,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(button_text, url=deep_link)]
                ])
            )

            # Auto delete message after 30 seconds
            asyncio.create_task(auto_delete(msg, delay=30))

        except RPCError as e:
            print(f"RPCError: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

async def auto_delete(msg, delay=30):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except Exception:
        pass
