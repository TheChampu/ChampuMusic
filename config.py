import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters
load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

BOT_TOKEN = getenv("BOT_TOKEN")

OWNER_USERNAME = getenv("OWNER_USERNAME","itsmeshivanshu")
BOT_USERNAME = getenv("BOT_USERNAME" , "@TheChampuBot")
# ---------------@TheChampu-----------------------------------------
BOT_NAME = getenv("BOT_NAME" , "TheChampuBot")
# ---------------------------------------------------------
ASSUSERNAME = getenv("ASSUSERNAME" , "itsmeshivanshu")

MONGO_DB_URI = getenv("MONGO_DB_URI", None)
#---------------------@TheChampu------------------------------------------
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))
# ------------------------@TheChampu----------------------------------------
LOGGER_ID = int(getenv("LOGGER_ID", None))
# --------------------------@TheChampu--------------------------------------
OWNER_ID = int(getenv("OWNER_ID", 6570546331))
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/TheChampu/ChampuMusic",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
# Maximum limit for fetching playlist's track from youtube, spotify, apple
# links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 2500))
# Maximum Limit Allowed for users to save playlists on bot's server
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", 100))
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
) 
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/akaChampu")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/TheChampuClub")
LOGGERS = "\x54\x68\x65\x43\x68\x61\x6D\x70\x75\x42\x6F\x74"
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "True")
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", 9000))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", 9999999))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", 9999999))
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "1c21247d714244ddbb09925dac565aed")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "709e1a2969664491b58200860623ef19")


#   ░█████╗░██╗░░██╗░█████╗░███╗░░░███╗██████╗░██╗░░░██╗
#   ██╔══██╗██║░░██║██╔══██╗████╗░████║██╔══██╗██║░░░██║
#   ██║░░╚═╝███████║███████║██╔████╔██║██████╔╝██║░░░██║
#   ██║░░██╗██╔══██║██╔══██║██║╚██╔╝██║██╔═══╝░██║░░░██║
#   ╚█████╔╝██║░░██║██║░░██║██║░╚═╝░██║██║░░░░░╚██████╔╝
#   ░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░░░░░╚═════╝░     



PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 5242880000))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 5242880000))
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)
STRING6 = getenv("STRING_SESSION6", None)
STRING7 = getenv("STRING_SESSION7", None)
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
START_IMG_URL = getenv(
    "START_IMG_URL", "https://telegra.ph/file/d3e855bc548a1ce9649e7.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://telegra.ph/file/33591be403ae3eaae7217.jpg"
)
PLAYLIST_IMG_URL = "https://telegra.ph/file/b860df3e144c2208a7e5a.jpg"
STATS_IMG_URL = "https://telegra.ph/file/a9d91437d795b0ae55af8.jpg"
TELEGRAM_AUDIO_URL = "https://telegra.ph/file/84492c50c7a8a8d2603dc.jpg"
TELEGRAM_VIDEO_URL = "https://telegra.ph/file/84492c50c7a8a8d2603dc.jpg"
STREAM_IMG_URL = "https://telegra.ph/file/62f26ca46103beee9a0d5.jpg"
SOUNCLOUD_IMG_URL = "https://telegra.ph/file/9fbc748ad0d552e403ba6.jpg"
YOUTUBE_IMG_URL = "https://telegra.ph/file/2433c1b98d2621623ead3.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://telegra.ph/file/38ae0f7b919a8995c7f29.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://telegra.ph/file/e17740f22da1fe4162e43.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://telegra.ph/file/010c936d41e9da782780f.jpg"
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
