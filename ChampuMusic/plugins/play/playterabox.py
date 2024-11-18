from pyrogram import filters
from pyrogram.types import Message
from ChampuMusic import app, TeraboxAPI  # Make sure to import your new TeraboxAPI
from ChampuMusic.core.call import Champu
from ChampuMusic.utils.database import is_active_chat
from ChampuMusic.utils.stream.queue import put_queue

terabox_api = TeraboxAPI()

@app.on_message(filters.command("playterabox") & filters.group)
async def play_terabox(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a Terabox link.")
        return

    link = message.command[1]

    # Validate the Terabox link
    if not await terabox_api.valid(link):
        await message.reply_text("Invalid Terabox link provided.")
        return

    # Fetch video details
    track_details, vidid = await terabox_api.track(link)
    if not track_details:
        await message.reply_text("Failed to fetch video details.")
        return


    title = track_details['title']
    duration_min = track_details['duration_min']
    user_id = message.from_user.id
    user_name = message.from_user.mention
    chat_id = message.chat.id
    original_chat_id = message.chat.id  # Adjust if needed

    # Check if there is an active chat
    if await is_active_chat(chat_id):
        await put_queue(
            chat_id,
            original_chat_id,
            vidid,
            title,
            duration_min,
            user_name,
            vidid,
            user_id,
            "video"  # Assuming it's a video
        )
        await message.reply_text(f"Added to queue: {title}")
    else:
        # If no active chat, join and play the video
        await Champu.join_call(chat_id, original_chat_id, link)  # Adjust if needed
        await put_queue(
            chat_id,
            original_chat_id,
            vidid,
            title,
            duration_min,
            user_name,
            vidid,
            user_id,
            "video"
        )
        await message.reply_text(f"Now playing: {title}")