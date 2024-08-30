from ChampuXMusic import app
from config import OWNER_ID
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ChampuXMusic.utils.Champu_ban import admin_filter

BOT_ID = "6399386263"

@app.on_message(filters.command("unbanall") & admin_filter)
async def unban_all(_, msg):
    chat_id = msg.chat.id
    x = 0
    bot = await app.get_chat_member(chat_id, BOT_ID)
    bot_permission = bot.privileges.can_restrict_members == True
    if bot_permission:
        banned_users = []
        async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
            banned_users.append(m.user.id)
            try:
                await app.unban_chat_member(chat_id, banned_users[x])
                print(f"ᴜɴʙᴀɴɪɴɢ ᴀʟʟ ᴍᴄ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ {m.user.mention}")
                x += 1
            except Exception:
                pass
    else:
        await msg.reply_text("ᴇɪᴛʜᴇʀ ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs ᴏʀ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ sᴜᴅᴏ ᴜsᴇʀs")

@app.on_callback_query(filters.regex("^stop$"))
async def stop_callback(_, query):
    await query.message.delete()

###
__MODULE__ = "Unbanall"
__HELP__ = """
**Unban All**

This module allows administrators to unban all users in a group at once.

Commands:
- /unbanall: Start unbanning all users in the group.

Note:
- Only administrators can use this command.
- The bot must have the necessary permissions to unban users.
"""