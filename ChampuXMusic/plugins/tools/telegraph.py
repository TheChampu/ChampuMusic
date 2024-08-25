from telegraph import upload_file
from pyrogram import filters
from ChampuXMusic import app
from pyrogram.types import InputMediaPhoto

@app.on_message(filters.command(["tgm" ]))
def ul(_, message):
    reply = message.reply_to_message
    if reply.media:
        i = message.reply("ᴍᴀᴋᴇ ʏᴏᴜʀ ʟɪɴᴋ...")
        path = reply.download()
        fk = upload_file(path)
        for x in fk:
            url = "https://telegra.ph" + x

        i.edit(f'ʜᴇʀᴇ ʏᴏᴜʀ ʟɪɴᴋ ʙᴀʙᴇ... {url}')