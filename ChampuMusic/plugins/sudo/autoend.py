from pyrogram import filters
from config import OWNER_ID
from strings import get_command
from ChampuMusic import app
from ChampuMusic.misc import SUDOERS, SPECIAL_ID
from ChampuMusic.utils.database import autoend_off, autoend_on

# Commands
AUTOEND_COMMAND = get_command("AUTOEND_COMMAND")


@app.on_message(filters.command(AUTOEND_COMMAND) & (filters.user(OWNER_ID) | filters.user(SPECIAL_ID)) & SUDOERS)
async def auto_end_stream(client, message):
    usage = "**ᴜsᴀɢᴇ:**\n\n/autoend [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await autoend_on()
        await message.reply_text(
            "Aᴜᴛᴏ Eɴᴅ Sᴛʀᴇᴀᴍ Eɴᴀʙʟᴇᴅ.\n\nBᴏᴛ ᴡɪʟʟ ʟᴇᴀᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀғᴛᴇʀ 3 ᴍɪɴs ɪғ ɴᴏ ᴏɴᴇ ɪs ʟɪsᴛᴇɴɪɴɢ ᴡɪᴛʜ ᴀ ᴡᴀʀɴɪɴɢ ᴍᴇssᴀɢᴇ.."
        )
    elif state == "disable":
        await autoend_off()
        await message.reply_text("ᴀᴜᴛᴏᴇɴᴅ ᴅɪsᴀʙʟᴇᴅ")
    else:
        await message.reply_text(usage)
