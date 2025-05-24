from ANNIEMUSIC.core.bot import JARVIS
from ANNIEMUSIC.core.dir import dirr
from ANNIEMUSIC.core.git import git
from ANNIEMUSIC.core.userbot import Userbot
from ANNIEMUSIC.logging import LOGGER
from config import SUDOERS

app = JARVIS()
userbot = Userbot()

from ANNIEMUSIC.platforms import (
    AppleAPI, CarbonAPI, SoundAPI, SpotifyAPI,
    RessoAPI, TeleAPI, YouTubeAPI
)

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

def initialize_all():
    dirr()
    git()
    from ANNIEMUSIC.misc import heroku, dbb
    dbb()
    heroku()
