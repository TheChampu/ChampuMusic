from SafoneAPI import SafoneAPI

from ChampuXMusic.core.bot import Champu
from ChampuXMusic.core.dir import dirr
from ChampuXMusic.core.git import git
from ChampuXMusic.core.userbot import Userbot
from ChampuXMusic.misc import dbb, heroku

from .logging import LOGGER

EMOJIS = ["PPLAY_1", "PPLAY_2", "PPLAY_3", "PPLAY_4", "PPLAY_5",
          "PPLAY_6", "PPLAY_7", "PPLAY_8", "PPLAY_9", "PPLAY_10",
          "PPLAY_11", "PPLAY_12", "PPLAY_13", "PPLAY_14", "PPLAY_15",
          "PPLAY_16", "PPLAY_17"]

dirr()
git()
dbb()
heroku()

app = Champu()
api = SafoneAPI()
userbot = Userbot()
HELPABLE = {}

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
APP = "\x54\x68\x65\x43\x68\x61\x6D\x70\x75\x42\x6F\x74"  # connect music api key "Dont change it"
