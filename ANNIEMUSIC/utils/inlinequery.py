from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

answer = [
    InlineQueryResultArticle(
        title="Pᴀᴜsᴇ",
        description="ᴩᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.",
        thumb_url="https://files.catbox.moe/mx5m1v.jpg",
        input_message_content=InputTextMessageContent("/pause"),
    ),
    InlineQueryResultArticle(
        title="Rᴇsᴜᴍᴇ",
        description="ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴩᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.",
        thumb_url="https://files.catbox.moe/mx5m1v.jpg",
        input_message_content=InputTextMessageContent("/resume"),
    ),
    InlineQueryResultArticle(
        title="Sᴋɪᴩ",
        description="sᴋɪᴩ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ ᴍᴏᴠᴇ ᴛᴏ ᴛʜᴇ ɴᴇxᴛ.",
        thumb_url="https://files.catbox.moe/mx5m1v.jpg",
        input_message_content=InputTextMessageContent("/skip"),
    ),
    InlineQueryResultArticle(
        title="Eɴᴅ",
        description="ᴇɴᴅ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ ᴏɴ ᴠᴄ.",
        thumb_url="https://files.catbox.moe/mx5m1v.jpg",
        input_message_content=InputTextMessageContent("/end"),
    ),
    InlineQueryResultArticle(
        title="Sʜᴜғғʟᴇ",
        description="sʜᴜғғʟᴇ ᴛʜᴇ ǫᴜᴇᴜᴇᴅ sᴏɴɢs.",
        thumb_url="https://files.catbox.moe/mx5m1v.jpg",
        input_message_content=InputTextMessageContent("/shuffle"),
    ),
    InlineQueryResultArticle(
        title="Lᴏᴏᴩ",
        description="ʟᴏᴏᴩ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴛʀᴀᴄᴋ ᴏɴ ʀᴇᴘᴇᴀᴛ.",
        thumb_url="https://files.catbox.moe/mx5m1v.jpg",
        input_message_content=InputTextMessageContent("/loop 3"),
    ),
]
