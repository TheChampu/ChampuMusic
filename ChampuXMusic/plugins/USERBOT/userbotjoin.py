import asyncio

from pyrogram import Client, filters

from ChampuXMusic.misc import SUDOERS
from ChampuXMusic.utils.database import get_assistant
from ChampuXMusic.utils.Champu_ban import admin_filter

links = {}


@Client.on_message(
    filters.command("userbotleave", prefixes=["."]) & filters.group & admin_filter
)
async def leave_one(client, message):
    try:
        userbot = await get_assistant(message.chat.id)
        await userbot.leave_chat(message.chat.id)
        await client.send_message(
            message.chat.id, "**✅ ᴜsᴇʀʙᴏᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ ᴛʜɪs Chat.**"
        )
    except Exception as e:
        print(e)


@Client.on_message(filters.command(["leaveall"], prefixes=["."]) & SUDOERS)
async def leave_all(client, message):
    if message.from_user.id not in SUDOERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **ᴜsᴇʀʙᴏᴛ** ʟᴇᴀᴠɪɴɢ ᴀʟʟ ᴄʜᴀᴛs !")
    try:
        userbot = await get_assistant(message.chat.id)
        async for dialog in userbot.get_dialogs():
            if dialog.chat.id == -1001733534088:
                continue
            try:
                await userbot.leave_chat(dialog.chat.id)
                left += 1
                await lol.edit(
                    f"**ᴜsᴇʀʙᴏᴛ ʟᴇᴀᴠɪɴɢ ᴀʟʟ ɢʀᴏᴜᴘ...**\n\n**ʟᴇғᴛ:** {left} ᴄʜᴀᴛs.\n**ғᴀɪʟᴇᴅ:** {failed} ᴄʜᴀᴛs."
                )
            except BaseException:
                failed += 1
                await lol.edit(
                    f"**ᴜsᴇʀʙᴏᴛ ʟᴇᴀᴠɪɴɢ...**\n\n**ʟᴇғᴛ:** {left} chats.\n**ғᴀɪʟᴇᴅ:** {failed} chats."
                )
            await asyncio.sleep(3)
    finally:
        await client.send_message(
            message.chat.id,
            f"**✅ ʟᴇғᴛ ғʀᴏᴍ:* {left} chats.\n**❌ ғᴀɪʟᴇᴅ ɪɴ:** {failed} chats.",
        )
