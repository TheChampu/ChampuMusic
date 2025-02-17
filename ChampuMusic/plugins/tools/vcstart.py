import asyncio
from typing import Optional, List, Union
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPrivileges
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.errors import UserAlreadyParticipant, ChatAdminRequired
from ChampuMusic import app
from ChampuMusic.core.call import Champu
from pytgcalls import StreamType
from pytgcalls.types import AudioPiped
from pytgcalls.exceptions import NoActiveGroupCall, AlreadyJoinedError
from ChampuMusic.utils.database import get_assistant, group_assistant

@app.on_message(filters.command(["vcinfo"], ["/", "!"]))
async def strcall(client: Client, message: Message):
    assistant = await group_assistant(Champu, message.chat.id)
    try:
        await assistant.join_group_call(
            message.chat.id,
            AudioPiped("./assets/call.mp3")
        )
        text = "- Beloveds in the call 🫶 :\n\n"
        participants = await assistant.get_participants(message.chat.id)
        for k, participant in enumerate(participants, start=1):
            user = await client.get_users(participant.user_id)
            mut = "ꜱᴘᴇᴀᴋɪɴɢ 🗣 " if not participant.muted else "ᴍᴜᴛᴇᴅ 🔕 "
            text += f"{k} ➤ {user.mention} ➤ {mut}\n"
        text += f"\nɴᴜᴍʙᴇʀ ᴏꜰ ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛꜱ : {len(participants)}"
        await message.reply(text)
        await asyncio.sleep(7)
        await assistant.leave_group_call(message.chat.id)
    except NoActiveGroupCall:
        await message.reply("ᴛʜᴇ ᴄᴀʟʟ ɪꜱ ɴᴏᴛ ᴏᴘᴇɴ ᴀᴛ ᴀʟʟ")
    except Exception as e:
        if "TelegramServerError" in str(e):
            await message.reply("ꜱᴇɴᴅ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴀɢᴀɪɴ, ᴛʜᴇʀᴇ ɪꜱ ᴀ ᴘʀᴏʙʟᴇᴍ ᴡɪᴛʜ ᴛʜᴇ ᴛᴇʟᴇɢʀᴀᴍ ꜱᴇʀᴠᴇʀ ❌")
        else:
            raise e
    except AlreadyJoinedError:
        text = "ʙᴇʟᴏᴠᴇᴅꜱ ɪɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ 🫶 :\n\n"
        participants = await assistant.get_participants(message.chat.id)
        for k, participant in enumerate(participants, start=1):
            user = await client.get_users(participant.user_id)
            mut = "ꜱᴘᴇᴀᴋɪɴɢ 🗣 " if not participant.muted else "ᴍᴜᴛᴇᴅ 🔕 "
            text += f"{k} ➤ {user.mention} ➤ {mut}\n"
        text += f"\nɴᴜᴍʙᴇʀ ᴏꜰ ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛꜱ : {len(participants)}"
        await message.reply(text)

async def get_group_call(client: Client, message: Message, err_msg: str = "") -> Optional[InputGroupCall]:
    assistant = await get_assistant(message.chat.id)
    chat_peer = await assistant.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await assistant.invoke(GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (await assistant.invoke(GetFullChat(chat_id=chat_peer.chat_id))).full_chat
        if full_chat is not None:
            return full_chat.call
    await app.send_message(message.chat.id, f"No group ᴠᴏɪᴄᴇ ᴄʜᴀᴛ Found** {err_msg}")
    return None

@app.on_message(filters.command(["vcstart", "startvc"], ["/", "!"]))
async def start_group_call(client: Client, message: Message):
    chat_id = message.chat.id
    assistant = await get_assistant(chat_id)
    if assistant is None:
        await app.send_message(chat_id, "ᴇʀʀᴏʀ ᴡɪᴛʜ ᴀꜱꜱɪꜱᴛᴀɴᴛ")
        return
    msg = await app.send_message(chat_id, "ꜱᴛᴀʀᴛɪɴɢ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ..")
    try:
        peer = await assistant.resolve_peer(chat_id)
        await assistant.invoke(
            CreateGroupCall(
                peer=InputPeerChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
                random_id=assistant.rnd_id() // 9000000000,
            )
        )
        await msg.edit_text("ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ꜱᴛᴀʀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ⚡️~!")
    except ChatAdminRequired:
        try:
            ass = await assistant.get_me()
            assid = ass.id
            await app.promote_chat_member(chat_id, assid, privileges=ChatPrivileges(
                can_manage_chat=False,
                can_delete_messages=False,
                can_manage_video_chats=True,
                can_restrict_members=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_promote_members=False,
            ))
            peer = await assistant.resolve_peer(chat_id)
            await assistant.invoke(
                CreateGroupCall(
                    peer=InputPeerChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
                    random_id=assistant.rnd_id() // 9000000000,
                )
            )
            await app.promote_chat_member(chat_id, assid, privileges=ChatPrivileges(
                can_manage_chat=False,
                can_delete_messages=False,
                can_manage_video_chats=False,
                can_restrict_members=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_promote_members=False,
            ))
            await msg.edit_text("ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ꜱᴛᴀʀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ⚡️~!")
        except:
            await msg.edit_text("ɢɪᴠᴇ ᴛʜᴇ ʙᴏᴛ ᴀʟʟ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ⚡")

@app.on_message(filters.command(["vcend", "endvc"], ["/", "!"]))
async def stop_group_call(client: Client, message: Message):
    chat_id = message.chat.id
    assistant = await get_assistant(chat_id)
    if assistant is None:
        await app.send_message(chat_id, "ᴇʀʀᴏʀ ᴡɪᴛʜ ᴀꜱꜱɪꜱᴛᴀɴᴛ")
        return
    msg = await app.send_message(chat_id, "ᴄʟᴏꜱɪɴɢ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ..")
    try:
        group_call = await get_group_call(assistant, message, err_msg=", ɢʀᴏᴜᴘ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴀʟʀᴇᴀᴅʏ ᴇɴᴅᴇᴅ")
        if not group_call:
            return
        await assistant.invoke(DiscardGroupCall(call=group_call))
        await msg.edit_text("ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴄʟᴏꜱᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ⚡️~!")
    except Exception as e:
        if "GROUPCALL_FORBIDDEN" in str(e):
            try:
                ass = await assistant.get_me()
                assid = ass.id
                await app.promote_chat_member(chat_id, assid, privileges=ChatPrivileges(
                    can_manage_chat=False,
                    can_delete_messages=False,
                    can_manage_video_chats=True,
                    can_restrict_members=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                ))
                group_call = await get_group_call(assistant, message, err_msg=", ɢʀᴏᴜᴘ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴀʟʀᴇᴀᴅʏ ᴇɴᴅᴇᴅ")
                if not group_call:
                    return
                await assistant.invoke(DiscardGroupCall(call=group_call))
                await app.promote_chat_member(chat_id, assid, privileges=ChatPrivileges(
                    can_manage_chat=False,
                    can_delete_messages=False,
                    can_manage_video_chats=False,
                    can_restrict_members=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                ))
                await msg.edit_text("ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴄʟᴏꜱᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ⚡️~!")
            except:
                await msg.edit_text("ɢɪᴠᴇ ᴛʜᴇ ʙᴏᴛ ᴀʟʟ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ")