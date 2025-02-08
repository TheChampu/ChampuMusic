from pyrogram.types import InlineKeyboardButton

import config
from config import SUPPORT_GROUP
from ChampuMusic import app


def start_pannel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_9"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_GROUP}"),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_5"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text=_["S_B_3"], url=config.SUPPORT_GROUP),
            InlineKeyboardButton(text=_["S_B_4"], url=config.SUPPORT_CHANNEL),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_1"], callback_data="settings_back_helper"
            )
        ],
    ]
    return buttons


def alive_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_9"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_GROUP}"),
        ],
    ]
    return buttons

# Start panel for inline buttons
def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["SO_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_GROUP),
        ],
    ]
    return buttons

def music_start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="❖ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ❖",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text="˹ᴀʙᴏᴜᴛ˼", callback_data="about"),
            InlineKeyboardButton(text="˹sᴜᴘᴘᴏʀᴛ˼", callback_data="support"),
        ],
        [InlineKeyboardButton(text="۞ ғᴇᴀᴛᴜʀᴇs ۞", callback_data="feature")],
    ]
    return buttons