import os
import cv2
from PIL import Image
from pyrogram import Client, filters
from ANNIEMUSIC import app

@app.on_message(filters.command("tiny"))
async def tiny_sticker(client, message):
    reply = message.reply_to_message
    if not (reply and reply.sticker):
        return await message.reply("Please reply to a sticker.")
    
    status = await message.reply("Processing...")

    try:
        downloaded_file = await app.download_media(reply)
        background = Image.open("ANNIEMUSIC/assets/rajnish.png")
        file_ext = os.path.splitext(downloaded_file)[-1].lower()

        if file_ext == ".tgs":
            os.system(f"lottie_convert.py {downloaded_file} json.json")
            with open("json.json", "r") as f:
                content = f.read().replace("512", "2000")
            with open("json.json", "w") as f:
                f.write(content)
            os.system("lottie_convert.py json.json wel2.tgs")
            file = "wel2.tgs"
            os.remove("json.json")

        elif file_ext in [".mp4"]:
            cap = cv2.VideoCapture(downloaded_file)
            ret, frame = cap.read()
            if not ret:
                return await status.edit("Failed to read video.")
            cv2.imwrite("frame.png", frame)
            image = Image.open("frame.png")
            file = process_image(image, background)
            os.remove("frame.png")

        else:
            image = Image.open(downloaded_file)
            file = process_image(image, background)

        await app.send_document(message.chat.id, file, reply_to_message_id=message.id)

    except Exception as e:
        await status.edit(f"Error: {e}")
        return

    finally:
        await status.delete()
        if os.path.exists(downloaded_file): os.remove(downloaded_file)
        if os.path.exists(file): os.remove(file)


def process_image(image, background):
    w, h = image.size
    if w == h:
        new_w, new_h = 200, 200
    else:
        total = w + h
        new_w = int(200 + 5 * ((w / total * 100) - 50))
        new_h = int(200 + 5 * ((h / total * 100) - 50))
    
    resized = image.resize((new_w, new_h))
    out_file = "output.webp"
    combined = background.copy()
    combined.paste(resized, (150, 0))
    combined.save(out_file, "WEBP", quality=95)
    return out_file
