from random import choice
from pyrogram import filters, Client
from pyrogram.types import Message
from ChampuMusic.misc import SUDOERS as SUDO_USER
from ChampuMusic.utils.data import RAID, PBIRAID, OneWord, HIRAID, PORM, EMOJI, GROUP, VERIFIED_USERS


ACTIVATE_RLIST = []


@Client.on_message(filters.command("rr", prefixes=".") & SUDO_USER)
async def rr(client: Client, message: Message):
    r = await message.edit_text("**Processing**")
    reply = message.reply_to_message
    if reply:
        user = reply.from_user.id
    else:
        user = message.text.split(None, 1)[1]
        if not user:
            await r.edit("**Provide Me A USER_ID or reply to someone**")
            return
    user = await client.get_users(user)
    if int(message.chat.id) in GROUP:
        await r.edit("`You Cannot Spam In Developers' Chat`")
        return
    if int(user.id) in VERIFIED_USERS:
        await r.edit("You Cannot Spam On Developers")
        return
    elif int(user.id) in SUDO_USER:
        await r.edit("That Guy Is part of sudo user.")
        return
    elif int(user.id) in ACTIVATE_RLIST:
        await r.edit("User Already in Raidlist.")
        return
    ACTIVATE_RLIST.append(user.id)
    await r.edit(f"**Replyraid Activated On {user.first_name} Successfully ✅**")

@Client.on_message(filters.command("drr", prefixes=".") & SUDO_USER)
async def drr(client: Client, message: Message):
    r = await message.edit_text("**Processing**")
    reply = message.reply_to_message
    if reply:
        user = reply.from_user.id
    else:
        user = message.text.split(None, 1)[1]
        if not user:
            await r.edit("Provide me username/userid or reply to user for deactivating replyraid")
            return
    user = await client.get_users(user)
    if int(user.id) not in ACTIVATE_RLIST:
        await r.edit("User Not in Replyraid.")
        return
    ACTIVATE_RLIST.remove(user.id)
    await r.edit(f"**Reply Raid has Been Removed {user.first_name}, enjoy!**")


@Client.on_message(filters.incoming)
async def watch_raids(client: Client, message: Message):
    try:
        if not message:
            return
        if not message.from_user:
            return
        user = message.from_user.id
        userr = message.from_user
        mention = f"[{userr.first_name}](tg://user?id={userr.id})"
        raid = f"{mention} {choice(RAID)}"
        if int(user) in VERIFIED_USERS:
            return
        elif int(user) in SUDO_USER:
            return
        if int(message.chat.id) in GROUP:
            return
        try:
            if not message.from_user.id in ACTIVATE_RLIST:
                return
        except AttributeError:
            return
        try:
            if message.from_user.id in ACTIVATE_RLIST:
                await message.reply_text(raid)
        except Exception as a:
            print(f"An error occurred (a): {str(a)}")
    except Exception as b:
        print(f"An error occurred (b): {str(b)}")