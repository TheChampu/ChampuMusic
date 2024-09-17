from ChampuMusic.core.bot import ChampuBot
from ChampuMusic.core.dir import dirr
from ChampuMusic.core.git import git
from ChampuMusic.core.userbot import Userbot
from ChampuMusic.misc import dbb, heroku, sudo

from .logging import LOGGER

# Bot Client
app = ChampuBot()

# Assistant Client
userbot = Userbot()

# Directories
dirr()

# Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

# Load Sudo Users from DB
sudo()


from .platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()
HELPABLE = {}
