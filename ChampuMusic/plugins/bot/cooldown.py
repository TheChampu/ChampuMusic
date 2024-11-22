from time import time
from functools import wraps
from pyrogram.types import Message

def cooldown(wait_time):
    last_clicked_times = {}

    def decorator(func):
        @wraps(func)
        async def wrapper(client, message: Message, *args, **kwargs):
            user_id = message.from_user.id
            now = time()
            
            
            if user_id in last_clicked_times and (now - last_clicked_times[user_id] < wait_time):
                await message.edit(f"ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ {int(wait_time - (now - last_clicked_times[user_id]))} sᴇᴄᴏɴᴅs ʙᴇғᴏʀᴇ ᴄʟɪᴄᴋɪɴɢ ᴀɢᴀɪɴ.", show_alert=True)
                return
            
            last_clicked_times[user_id] = now
            return await func(client, message, *args, **kwargs)
        
        return wrapper
    return decorator