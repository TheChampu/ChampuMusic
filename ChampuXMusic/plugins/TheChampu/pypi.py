from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from ChampuXMusic import app


def get_pypi_info(package_name):
    try:
        
        api_url = f"https://pypi.org/pypi/{package_name}/json"
        
        # Sending a request to the PyPI API
        response = requests.get(api_url)
        
        # Extracting information from the API response
        pypi_info = response.json()
        
        return pypi_info
    
    except Exception as e:
        print(f"ᴇʀʀᴏʀ ғᴇᴛᴄʜɪɴɢ ᴘʏᴘɪ ɪɴғᴏʀᴍᴀᴛɪᴏɴ: {e}")
        return None

@app.on_message(filters.command("pypi", prefixes="/"))
def pypi_info_command(client, message):
    try:
       
        package_name = message.command[1]
        
        # Getting information from PyPI
        pypi_info = get_pypi_info(package_name)
        
        if pypi_info:
            # Creating a message with PyPI information
            info_message = f"ᴘᴀᴄᴋᴀɢᴇ ɴᴀᴍᴇ ➪ {pypi_info['info']['name']}\n\n" \
                           f"ʟᴀᴛᴇsᴛ ᴠɪʀsɪᴏɴ➪ {pypi_info['info']['version']}\n\n" \
                           f"ᴅᴇsᴄʀɪᴘᴛɪᴏɴ➪ {pypi_info['info']['summary']}\n\n" \
                           f"ᴘʀᴏᴊᴇᴄᴛ ᴜʀʟ➪ {pypi_info['info']['project_urls']['Homepage']}"
            
            # Sending the PyPI information back to the user
            client.send_message(message.chat.id, info_message)
        
        else:
            # Handling the case where information retrieval failed
            client.send_message(message.chat.id, "ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ғʀᴏᴍ ᴘʏᴘɪ.")
    
    except IndexError:

        client.send_message(message.chat.id, "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴘᴀᴄᴋᴀɢᴇ ɴᴀᴍᴇ ᴀғᴛᴇʀ ᴛʜᴇ /pypi ᴄᴏᴍᴍᴀɴᴅ.")
