from ... import *
from pyrogram import *
from pyrogram.types import *


@app.on_message(filters.command(["bin", "ccbin", "bininfo"], [".", "!", "/"]))
async def check_ccbin(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "<b>ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴍᴇ ᴀ ʙɪɴ ᴛᴏ\ɴɢᴇᴛ ʙɪɴ ᴅᴇᴛᴀɪʟs !</b>"
        )
    try:
        await message.delete()
    except:
        pass
    aux = await message.reply_text("<b>ᴄʜᴇᴄᴋɪɴɢ ...</b>")
    bin = message.text.split(None, 1)[1]
    if len(bin) < 6:
        return await aux.edit("<b>❌ᴡʀᴏɴɢ ʙɪɴ❗...</b>")
    try:
        resp = await api.bininfo(bin)
        await aux.edit(f"""
<b>💠 ʙɪɴ ғᴜʟʟ ᴅᴇᴛᴀɪʟs:</b>

<b>🏦 Bank:</b> <tt>{resp.bank}</tt>
<b>💳 Bin:</b> <tt>{resp.bin}</tt>
<b>🏡 Country:</b> <tt>{resp.country}</tt>
<b>🇮🇳 Flag:</b> <tt>{resp.flag}</tt>
<b>🧿 ISO:</b> <tt>{resp.iso}</tt>
<b>⏳ Level:</b> <tt>{resp.level}</tt>
<b>🔴 Prepaid:</b> <tt>{resp.prepaid}</tt>
<b>🆔 Type:</b> <tt>{resp.type}</tt>
<b>ℹ️ Vendor:</b> <tt>{resp.vendor}</tt>"""
        )
    except:
        return await aux.edit(f"""
🚫 BIN not recognized. Please enter a valid BIN.""")
