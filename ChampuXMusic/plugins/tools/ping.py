from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from config import *
from ChampuXMusic import app
from ChampuXMusic.core.call import Champu
from ChampuXMusic.utils import bot_sys_stats
from ChampuXMusic.utils.decorators.language import language
from ChampuXMusic.utils.inline import supp_markup
from config import BANNED_USERS


@app.on_message(filters.command("ping", prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_video(
        video="https://graph.org/file/5690109178f081adf464d.mp4",
        caption=_["ping_1"].format(app.mention),
    )
    pytgping = await Champu.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )


__MODULE__ = "Ping"
__HELP__ = """
## Ping Command Help

**Description:**
This command measures the ping of the bot and displays system information.

**Usage:**
/ping

**Details:**
- Measures the ping of the bot.
- Displays system information such as uptime, CPU usage, RAM usage, disk usage, and ping to the Telegram servers.
- Shows the ping in a graphical format.
- Provides buttons for navigation to the bot group, more information, and help.

**Examples:**
- `/ping`

"""
