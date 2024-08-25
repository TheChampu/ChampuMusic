import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from ChampuXMusic import app
from ChampuXMusic.mongo.afkdb import LOGGERS as OWNERS
from ChampuXMusic.utils.database import add_served_chat, get_assistant


start_txt = """**
✪ 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗖𝗵𝗮𝗺𝗽𝘂 𝗥𝗲𝗽𝗼𝘀 ✪

➲ ᴇᴀsʏ ʜᴇʀᴏᴋᴜ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ ✰  
➲ ɴᴏ ʙᴀɴ ɪssᴜᴇs ✰  
➲ ᴜɴʟɪᴍɪᴛᴇᴅ ᴅʏɴᴏs ✰  
➲ 𝟸𝟺/𝟽 ʟᴀɢ-ғʀᴇᴇ ✰

► sᴇɴᴅ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ɪғ ʏᴏᴜ ғᴀᴄᴇ ᴀɴʏ ᴘʀᴏʙʟᴇᴍs!
**"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{app.username}?startgroup=true")
        ],
        [
          InlineKeyboardButton("ᴄʜᴧᴍᴘᴜ", url="https://t.me/TheChampu"),
          InlineKeyboardButton("sʜɪᴠᴀɴsʜᴜ", url="https://t.me/TheShivanshu"),
          ],
               [
                InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/itsmeshivanshu"),

],
[
              InlineKeyboardButton("ᴍᴜsɪᴄ", url=f"https://github.com/TheChampu/ChampuMusic"),
              InlineKeyboardButton("sᴛʀɪɴɢ", url=f"https://github.com/TheChampu/ChampuXString"),
              ],
              [
              InlineKeyboardButton("ᴍᴀɴᴀɢᴍᴇɴᴛ", url=f"https://github.com/TheChampu/ChampuXManagment"),
InlineKeyboardButton("ᴄʜᴀᴛʙᴏᴛ", url=f"https://github.com/TheChampu/ChatBot"),
]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo=config.START_IMG_URL,
        caption=start_txt,
        reply_markup=reply_markup
    )


@app.on_message(filters.command("clone"))
async def clones(client: Client, message: Message):
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=f"""**ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ sᴜᴅᴏ ᴜsᴇʀ sᴏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴄʟᴏɴᴇ ᴍᴇ.**\n**ᴄʟɪᴄᴋ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴀɴᴅ ʜᴏsᴛ ᴍᴀɴᴜᴀʟʟʏ ᴏᴛʜᴇʀᴡɪsᴇ ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ ᴏʀ sᴜᴅᴏ ᴜsᴇʀs ғᴏʀ ᴄʟᴏɴᴇ.**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "sᴏᴜʀᴄᴇ", url=f"https://github.com/TheChampu/ChampuXMusic"
                    )
                ]
            ]
        ),
    )


# --------------------------------------------------------------------------------- #


@app.on_message(
    filters.command(
        ["hi", "hii", "hello", "hui", "good", "gm", "ok", "bye", "welcome", "thanks"],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
    & filters.group
)
async def bot_check(_, message):
    chat_id = message.chat.id
    await add_served_chat(chat_id)


# --------------------------------------------------------------------------------- #


import asyncio


@app.on_message(filters.command("gadd") & filters.user(int(OWNERS)))
async def add_allbot(client, message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 2:
        await message.reply(
            "**⚠️ ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ғᴏʀᴍᴀᴛ. ᴘʟᴇᴀsᴇ ᴜsᴇ ʟɪᴋᴇ » `/gadd @TheChampuBot`**"
        )
        return

    bot_username = command_parts[1]
    try:
        userbot = await get_assistant(message.chat.id)
        bot = await app.get_users(bot_username)
        app_id = bot.id
        done = 0
        failed = 0
        lol = await message.reply("🔄 **ᴀᴅᴅɪɴɢ ɢɪᴠᴇɴ ʙᴏᴛ ɪɴ ᴀʟʟ ᴄʜᴀᴛs!**")
        await userbot.send_message(bot_username, f"/start")
        async for dialog in userbot.get_dialogs():
            if dialog.chat.id == -1002120144597:
                continue
            try:

                await userbot.add_chat_members(dialog.chat.id, app_id)
                done += 1
                await lol.edit(
                    f"**🔂 ᴀᴅᴅɪɴɢ {bot_username}**\n\n**➥ ᴀᴅᴅᴇᴅ ɪɴ {done} ᴄʜᴀᴛs ✅**\n**➥ ғᴀɪʟᴇᴅ ɪɴ {failed} ᴄʜᴀᴛs ❌**\n\n**➲ ᴀᴅᴅᴇᴅ ʙʏ»** @{userbot.username}"
                )
            except Exception as e:
                failed += 1
                await lol.edit(
                    f"**🔂 ᴀᴅᴅɪɴɢ {bot_username}**\n\n**➥ ᴀᴅᴅᴇᴅ ɪɴ {done} ᴄʜᴀᴛs ✅**\n**➥ ғᴀɪʟᴇᴅ ɪɴ {failed} ᴄʜᴀᴛs ❌**\n\n**➲ ᴀᴅᴅɪɴɢ ʙʏ»** @{userbot.username}"
                )
            await asyncio.sleep(3)  # Adjust sleep time based on rate limits

        await lol.edit(
            f"**➻ {bot_username} ʙᴏᴛ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ🎉**\n\n**➥ ᴀᴅᴅᴇᴅ ɪɴ {done} ᴄʜᴀᴛs ✅**\n**➥ ғᴀɪʟᴇᴅ ɪɴ {failed} ᴄʜᴀᴛs ❌**\n\n**➲ ᴀᴅᴅᴇᴅ ʙʏ»** @{userbot.username}"
        )
    except Exception as e:
        await message.reply(f"Error: {str(e)}")