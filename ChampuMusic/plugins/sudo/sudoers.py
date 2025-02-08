from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from ChampuMusic import app
from pyrogram.types import InputMediaVideo
from ChampuMusic.misc import SUDOERS, SPECIAL_ID, SPECIAL_ID
from ChampuMusic.utils.database import add_sudo, remove_sudo
from ChampuMusic.utils.decorators.language import language
from ChampuMusic.utils.functions import extract_user
from ChampuMusic.utils.inline import close_markup
from config import BANNED_USERS, OWNER_ID
import logging

@app.on_message(filters.command(["addsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & (filters.user(OWNER_ID) | filters.user(SPECIAL_ID)))
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id in SUDOERS:
        return await message.reply_text(_["sudo_1"].format(user.mention))
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(_["sudo_2"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])

@app.on_message(filters.command(["delsudo", "rmsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & (filters.user(OWNER_ID) | filters.user(SPECIAL_ID)))
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id not in SUDOERS:
        return await message.reply_text(_["sudo_3"].format(user.mention))
    if user.id == SPECIAL_ID:
        return await message.reply_text("ʏᴏᴜ ᴄᴀɴɴᴏᴛ ʀᴇᴍᴏᴠᴇ ᴛʜɪs sᴘᴇᴄɪᴀʟ ᴜsᴇʀ.")
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(_["sudo_4"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])

@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & ~BANNED_USERS)
async def sudoers_list(client, message: Message):
    keyboard = [[InlineKeyboardButton("๏ ᴠɪᴇᴡ sᴜᴅᴏʟɪsᴛ ๏", callback_data="check_sudo_list")]]
    reply_markups = InlineKeyboardMarkup(keyboard)
    await message.reply_video(video="https://telegra.ph/file/3c9b53024f150d99032e1.mp4", caption="**» ᴄʜᴇᴄᴋ sᴜᴅᴏ ʟɪsᴛ ʙʏ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ.**\n\n**» ɴᴏᴛᴇ:**  ᴏɴʟʏ sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ ᴠɪᴇᴡ. ", reply_markup=reply_markups)
    

@app.on_callback_query(filters.regex("^check_sudo_list$"))
async def check_sudo_list(client, callback_query: CallbackQuery):
    keyboard = []
    if callback_query.from_user.id not in SUDOERS:
        return await callback_query.answer("sᴏʀʀʏ ʏᴀᴀʀ sɪʀғ ᴏᴡɴᴇʀ ᴏʀ sᴜᴅᴏ ᴡᴀʟᴇ ʜɪ sᴜᴅᴏʟɪsᴛ ᴅᴇᴋʜ sᴀᴋᴛᴇ ʜᴀɪ", show_alert=True)
    else:
        user = await app.get_users(OWNER_ID)

        # Ensure user is a single object and handle it accordingly
        if isinstance(user, list):
            user_mention = ", ".join([u.mention for u in user if hasattr(u, 'mention')]) or "Unknown User"
        else:
            user_mention = user.mention if hasattr(user, 'mention') else user.first_name

        caption = f"**˹ʟɪsᴛ ᴏғ ʙᴏᴛ ᴍᴏᴅᴇʀᴀᴛᴏʀs˼**\n\n**🌹Oᴡɴᴇʀ** ➥ {user_mention}\n\n"

        keyboard.append([InlineKeyboardButton("๏ ᴠɪᴇᴡ ᴏᴡɴᴇʀ ๏", url=f"tg://openmessage?user_id={OWNER_ID}")])
        
        count = 1
        for user_id in SUDOERS:
            if user_id != OWNER_ID and user_id != SPECIAL_ID:
                try:
                    user = await app.get_users(user_id)
                    if isinstance(user, list):
                        user_mention = ", ".join([u.mention for u in user if hasattr(u, 'mention')]) or "Unknown User"
                    else:
                        user_mention = user.mention if hasattr(user, 'mention') else user.first_name
                    caption += f"🎁 Sᴜᴅᴏ {count} » {user_mention} `{user_id}`\n"
                    count += 1
                except Exception as e:
                    continue

        # Add a "Back" button at the end
        keyboard.append([InlineKeyboardButton("๏ ʙᴀᴄᴋ ๏", callback_data="back_to_main_menu")])

        await callback_query.edit_message_text(caption, reply_markup=InlineKeyboardMarkup(keyboard))

@app.on_callback_query(filters.regex("^back_to_main_menu$"))
async def back_to_main_menu(client, callback_query: CallbackQuery):
    keyboard = [[InlineKeyboardButton("๏ ᴠɪᴇᴡ sᴜᴅᴏʟɪsᴛ ๏", callback_data="check_sudo_list")]]
    reply_markupes = InlineKeyboardMarkup(keyboard)
    await callback_query.message.edit_caption(caption="**» ᴄʜᴇᴄᴋ sᴜᴅᴏ ʟɪsᴛ ʙʏ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ.**\n\n**» ɴᴏᴛᴇ:**  ᴏɴʟʏ sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ ᴠɪᴇᴡ. ", reply_markup=reply_markupes)

@app.on_message(filters.command(["delallsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
@language
async def del_all_sudo(client, message: Message, _):
    removed_users = []  # List to store removed users' information
    for user_id in SUDOERS.copy():
        if user_id != OWNER_ID and user_id != SPECIAL_ID:
            removed = await remove_sudo(user_id)
            if removed:
                SUDOERS.remove(user_id)
                try:
                    user = await app.get_users(user_id)
                    user_mention = user.mention if user else f"ᴜsᴇʀ ɪᴅ: `{user_id}`"
                    removed_users.append(f"{user_mention} `{user_id}`")
                except Exception as e:
                    logging.error(f"ᴇʀʀᴏʀ ғᴇᴛᴄʜɪɴɢ ᴜsᴇʀ {user_id}: {e}")
                    removed_users.append(f"ᴜsᴇʀ ɪᴅ: `{user_id}`")

    if removed_users:
        removed_users_text = "\n".join(removed_users)
        await message.reply_text(f"ʀᴇᴍᴏᴠᴇᴅ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴜsᴇʀs ғʀᴏᴍ ᴛʜᴇ sᴜᴅᴏ ʟɪsᴛ:\n\n{removed_users_text}")
    else:
        await message.reply_text("ɴᴏ ᴜsᴇʀs ᴡᴇʀᴇ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴛʜᴇ sᴜᴅᴏ ʟɪsᴛ.")