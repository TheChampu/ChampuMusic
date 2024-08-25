from ChampuXMusic.core.bot import Champu
from ChampuXMusic.core.dir import dirr
from ChampuXMusic.core.git import git
from ChampuXMusic.core.userbot import Userbot
from ChampuXMusic.misc import dbb, heroku

from SafoneAPI import SafoneAPI
from .logging import LOGGER

PH_ON = ["https://telegra.ph/file/010c936d41e9da782780f.jpg",
         "https://telegra.ph/file/e17740f22da1fe4162e43.jpg",
         "https://telegra.ph/file/38ae0f7b919a8995c7f29.jpg",
         "https://telegra.ph/file/9fbc748ad0d552e403ba6.jpg",
         "https://telegra.ph/file/2433c1b98d2621623ead3.jpg",
         "https://telegra.ph/file/62f26ca46103beee9a0d5.jpg",
         "https://telegra.ph/file/d3e855bc548a1ce9649e7.jpg",
         "https://telegra.ph/file/b860df3e144c2208a7e5a.jpg",
         "https://telegra.ph/file/33591be403ae3eaae7217.jpg",
         "https://telegra.ph/file/a9d91437d795b0ae55af8.jpg",
         "https://telegra.ph/file/1891e318996f393e0aebc.jpg",
         "https://telegra.ph/file/84492c50c7a8a8d2603dc.jpg",
         "https://telegra.ph/file/ae843fb1e51218521e95b.jpg",
         "https://telegra.ph/file/0b98ff58d75e85438d3a0.jpg"]

VID_EO = ["https://telegra.ph/file/89c5023101b65f21fb401.mp4",
          "https://telegra.ph/file/bbc914cce6cce7f607641.mp4",
          "https://telegra.ph/file/abc578ecc222d28a861ba.mp4",
          "https://telegra.ph/file/065f40352707e9b5b7c15.mp4",
          "https://telegra.ph/file/52ceaf02eae7eed6c9fff.mp4",
          "https://telegra.ph/file/299108f6ac08f4e65e47a.mp4",
          "https://telegra.ph/file/7a4e08bd04d628de71fc1.mp4",
          "https://telegra.ph/file/0ad8b932fe5f7684f941c.mp4",
          "https://telegra.ph/file/95ebe2065cfb1ac324a1c.mp4",
          "https://telegra.ph/file/98cf22ccb987f9fedac5e.mp4",
          "https://telegra.ph/file/f1b1754fc9d01998f24df.mp4",
          "https://telegra.ph/file/421ee22ed492a7b8ce101.mp4"]

STKR = ["CAACAgUAAx0Ccg5OnAACO7Zmsgyr0PLz9JWrMk3Qq_nMVGgGfAACIQoAAkCj8Fdxa8YvGPC9nx4E" , 
        "CAACAgUAAx0Ccg5OnAACO7lmsgy3AUQHAW7G05yl_rf6Pb469gACZQgAAj3k-Vfsu_WmA6PiUx4E" , 
        "CAACAgUAAx0Ccg5OnAACO7xmsgzKSD0pzxgH8KFGaSQ9zifkJgACBAgAAgz1-Fdx5iMD0Bh8mR4E" , 
        "CAACAgUAAx0Ccg5OnAACO79msgzapLLbvhL2GZUX1ZPAs3QnwgACbQcAAj5O-Vfacb2S2B5RQB4E" , 
        "CAACAgUAAx0Ccg5OnAACO8JmsgztO7-hwSVQUuxKdjMeSglEqwACsAYAAgMG-Vd0t6HAhNHB5x4E" , 
        "CAACAgUAAx0Ccg5OnAACO8Vmsgz9z6YrW7xWS2cE9UsdbZvvRAACIwkAAlmS8FcdZ3xHfo764h4E" ,
        "CAACAgUAAx0Ccg5OnAACO8hmsg0TIO_DQ4FdyyMmtvqIp5g4FgAC1wcAAjJP-Vdg1wymsgazNB4E" , 
        "CAACAgEAAx0Ccg5OnAACO85msg1m3fnsbowqLGzlVblcH-7XsQAC1AUAAklTqUQlhMqMLBaIzR4E" , 
        "CAACAgEAAx0Ccg5OnAACO9Fmsg2MKg4OyLYRS_m3HaAazbIfngACYQQAAoD4qER5uOGwdDS1Nh4E"]

AFKSTKR = ["CAACAgUAAx0Ccg5OnAACO-BmshOSuYgFX-5DR-y85iWyuxNR4AACOwgAAna7gFYNBSEcBeyx6R4E" , 
           "CAACAgIAAx0Ccg5OnAACO-NmshOqrgABt5vehH3RmP38o3DNCW8AAgUAA8A2TxP5al-agmtNdR4E" , 
           "CAACAgIAAx0Ccg5OnAACO-ZmshO-lC0AAYOwg5VVvBBEkzSVaXkAAuEAA1KJkSM5wTa2R1-UzB4E"]


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