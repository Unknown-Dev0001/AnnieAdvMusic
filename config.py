import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# ───── Basic Bot Configuration ───── #
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

OWNER_ID = int(getenv("OWNER_ID", 7500269454))
OWNER_USERNAME = getenv("OWNER_USERNAME", "Unknown_RK01")
BOT_USERNAME = getenv("BOT_USERNAME", "LyraTuneBot")
BOT_NAME = getenv("BOT_NAME", "˹𝐋𝐫𝐲𝐚 ✘ 𝙼ᴜsɪᴄ˼ ♪")
ASSUSERNAME = getenv("ASSUSERNAME", "MoonKnight_official")
EVALOP = list(map(int, getenv("EVALOP", "8055384069").split()))

# ───── Mongo & Logging ───── #
MONGO_DB_URI = getenv("MONGO_DB_URI")
LOGGER_ID = int(getenv("LOGGER_ID", -1002441811198))

# ───── Limits and Durations ───── #
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))

# ───── Custom API Configs ───── #
API_URL = getenv("API_URL") # optional
API_KEY = getenv("API_KEY") # optional
COOKIE_URL = getenv("COOKIE_URL") # necessary
DEEP_API = getenv("DEEP_API") # optional

# ───── Heroku Configuration ───── #
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ───── Git & Updates ───── #
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/Unknown-Dev0001/ANNIE-X-MUSIC")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "Master")
GIT_TOKEN = getenv("GIT_TOKEN")

# ───── Support & Community ───── #
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/BotVerseRavi")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/BotVerseRaviSupport")

# ───── Assistant Auto Leave ───── #
AUTO_LEAVING_ASSISTANT = False
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "11500"))

# ───── Error Handling ───── #
DEBUG_IGNORE_LOG = True

# ───── Spotify Credentials ───── #
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "1281122466184cafa5c42259671f77ae")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "367311c34d5a4e8998ed5874b3fac0b8")

# ───── Session Strings ───── #
STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")

# ========= PORT ========= #
WEB_SERVER = bool(getenv("WEB_SERVER", True))
PING_URL = getenv("PING_URL")  # add your koyeb/render's public url
PING_TIME = int(getenv("PING_TIME"))  # Add timeout in seconds

# ───── Server Settings ───── #
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "3000"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "2500"))

# ───── Bot Media Assets ───── #

START_VIDS = [
    "https://telegra.ph/file/9b7e1b820c72a14d90be7.mp4",
    "https://telegra.ph/file/72f349b1386d6d9374a38.mp4",
    "https://telegra.ph/file/a4d90b0cb759b67d68644.mp4"
]

STICKERS = [
    "CAACAgUAAx0Cd6nKUAACASBl_rnalOle6g7qS-ry-aZ1ZpVEnwACgg8AAizLEFfI5wfykoCR4h4E",
    "CAACAgUAAx0Cd6nKUAACATJl_rsEJOsaaPSYGhU7bo7iEwL8AAPMDgACu2PYV8Vb8aT4_HUPHgQ"
]
HELP_IMG_URL = "https://ar-hosting.pages.dev/1747274242184.jpg"
PING_VID_URL = "https://ar-hosting.pages.dev/1745492565242.mp4"
PLAYLIST_IMG_URL = "https://ar-hosting.pages.dev/1745840374338.jpg"
STATS_VID_URL = "https://ar-hosting.pages.dev/1745492501123.mp4"
TELEGRAM_AUDIO_URL = "https://ar-hosting.pages.dev/1745840374338.jpg"
TELEGRAM_VIDEO_URL = "https://ar-hosting.pages.dev/1745840374338.jpg"
STREAM_IMG_URL = "https://ar-hosting.pages.dev/1745840374338.jpg"
SOUNCLOUD_IMG_URL = "https://ar-hosting.pages.dev/1745840374338.jpg"
YOUTUBE_IMG_URL = "https://ar-hosting.pages.dev/1745840374338.jpg"
SPOTIFY_ARTIST_IMG_URL = SPOTIFY_ALBUM_IMG_URL = SPOTIFY_PLAYLIST_IMG_URL = YOUTUBE_IMG_URL

# ───── Utility & Functional ───── #
def time_to_seconds(time: str) -> int:
    return sum(int(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))

DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")

# ───── Bot Introduction Messages ───── #
AYU = ["💞", "🦋", "🔍", "🧪", "⚡️", "🔥", "🎩", "🌈", "🍷", "🥂", "🥃", "🕊️", "🪄", "💌", "🧨"]
AYUV = [
    "❖ нєу {0},\n\n๏ ᴛʜɪs ɪs {1}!\n\n๏ ᴀ ғᴀsᴛ & ᴘᴏᴡᴇʀғᴜʟ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ᴡɪᴛʜ sᴏᴍᴇ ᴀᴡᴇsᴏᴍᴇ ғᴇᴀᴛᴜʀᴇs.\n\n•──────────────────•\n**๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs.**\n\n🫧 ᴅᴇᴠᴇʟᴏᴩᴇʀ 🪽 ➪ [ℛ𝒶𝓋𝒾 𝒦𝓊𝓂𝒶𝓇](https://t.me/Unknown_RK01)",
]

# ───── Runtime Structures ───── #
BANNED_USERS = filters.user()
adminlist, lyrical, votemode, autoclean, confirmer = {}, {}, {}, [], {}

# ───── URL Validation ───── #
if SUPPORT_CHANNEL and not re.match(r"^https?://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHANNEL URL. Must start with https://")

if SUPPORT_CHAT and not re.match(r"^https?://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHAT URL. Must start with https://")

# ───── SUDO USERS ───── #
SUDOERS = {OWNER_ID}  # Add more user IDs if needed
