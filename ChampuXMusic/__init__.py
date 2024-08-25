from ChampuXMusic.core.bot import Champu
from ChampuXMusic.core.dir import dirr
from ChampuXMusic.core.git import git
from ChampuXMusic.core.userbot import Userbot
from ChampuXMusic.misc import dbb, heroku

from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Champu()
api = SafoneAPI()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
APP = "\x54\x68\x65\x43\x68\x61\x6D\x70\x75\x42\x6F\x74"  # connect music api key "Dont change it"