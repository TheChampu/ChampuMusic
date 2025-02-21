import asyncio
import glob
import os
import random
import logging
import json
import time
from typing import Union
from config import OWNER_ID
from pyrogram import filters
from yt_dlp import YoutubeDL

from ChampuMusic import app
from ChampuMusic.misc import SUDOERS, SPECIAL_ID

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global YouTube token data
YOUTUBE = {
    "access_token": "ya29.a0AXeO80QLPVs5p7h_E7caxmPcVRG82MkGuILze6FWi6gGFVWTRdjaq8jBP02PvRAlAewi9PidTZNEsdWsi1_EnvYhroWjXJSJ1oG1-E029eBU1-lKVgPWiIFPbetScImSXl0I8WZqvedUO_5DvUIpoxhO2NtWTgBJ7879-NjfQzNMiSJzE2xbaCgYKATcSARISFQHGX2MiPXAOG-hTrmIUocJ9aqKW5Q0187",
    "expires": 1740224406.703791,
    "refresh_token": "1//05tJV9kJp7hsJCgYIARAAGAUSNwF-L9Irdpc0e9mqHJNQPg72hB-iY6VTGStBevutF3NVuYaAXHlgshkB3ufbZnJvSdsw8hheugc",
    "token_type": "Bearer"
}

COOKIES_FILE = "cookies/cookies.txt"

def TheChampu():
    TOKEN_DATA = os.getenv("TOKEN_DATA")
    if not TOKEN_DATA:
        os.environ["TOKEN_DATA"] = json.dumps(YOUTUBE)

def update_youtube_token(new_token_data: dict):
    """
    Updates the global YOUTUBE dictionary and environment variable with new token data.
    """
    global YOUTUBE
    YOUTUBE.update(new_token_data)
    os.environ["TOKEN_DATA"] = json.dumps(YOUTUBE)
    logger.info("YouTube token data updated successfully.")

def generate_new_auth_token():
    """
    Simulates generating a new auth token and updates the global YOUTUBE dictionary.
    Replace this with actual logic to generate a new token.
    """
    # Placeholder for generating new token data
    new_token_data = {
        "access_token": "new_access_token_here",
        "expires": time.time() + 3600,  # 1 hour from now
        "refresh_token": "new_refresh_token_here",
        "token_type": "Bearer"
    }

    # Update the global YOUTUBE dictionary and environment variable
    update_youtube_token(new_token_data)
    logger.info("New auth token generated and updated.")

def get_random_cookie():
    folder_path = os.path.join(os.getcwd(), "cookies")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.warning(f"Created cookies directory at {folder_path}")
        return None

    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    if not txt_files:
        logger.error("No .txt files found in the specified folder.")
        return None
    return random.choice(txt_files)

class YouTubeAuthDownloader:
    def __init__(self):
        self.base_url = "https://www.youtube.com/watch?v="

    def get_ytdl_options(self, ytdl_opts, auth_token: str) -> Union[str, dict, list]:
        if isinstance(ytdl_opts, list):
            ytdl_opts += ["--username", "oauth2", "--password", auth_token]
        elif isinstance(ytdl_opts, str):
            ytdl_opts += f"--username oauth2 --password {auth_token} "
        elif isinstance(ytdl_opts, dict):
            ytdl_opts.update({"username": "oauth2", "password": auth_token})
        return ytdl_opts

    async def download(self, link: str, auth_token: str, video: bool = True) -> str:
        loop = asyncio.get_running_loop()

        def download_content():
            ydl_opts = {
                "format": (
                    "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])"
                    if video
                    else "bestaudio/best"
                ),
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
            }
            ydl_opts = self.get_ytdl_options(ydl_opts, auth_token)

            ydl = YoutubeDL(ydl_opts)
            info = ydl.extract_info(link, download=False)
            file_path = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if not os.path.exists(file_path):
                ydl.download([link])
            return file_path

        try:
            file_path = await loop.run_in_executor(None, download_content)
            return file_path
        except Exception as e:
            logger.error(f"Failed to download content: {e}")
            raise

async def check_cookies(video_url):
    cookie_file = get_random_cookie()
    if not cookie_file:
        return False

    opts = {
        "format": "bestaudio",
        "quiet": True,
        "cookiefile": cookie_file,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl.extract_info(video_url, download=False)
        return True
    except Exception as e:
        logger.error(f"Cookie check failed: {e}")
        return False

async def check_auth_token():
    video_url = "https://www.youtube.com/watch?v=LLF3GMfNEYU"
    auth_token = os.getenv("TOKEN_DATA")
    if not auth_token:
        logger.error("Auth token not found in environment variables.")
        return False

    opts = {
        "format": "bestaudio",
        "quiet": True,
        "username": "oauth2",
        "password": auth_token,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl.extract_info(video_url, download=False)
        return True
    except Exception as e:
        logger.error(f"Auth token check failed: {e}")
        return False

@app.on_message(
    filters.command(
        [
            "authstatus",
            "authtoken",
            "cookies",
            "cookie",
            "cookiesstatus",
            "cookiescheck",
        ]
    )
    & SUDOERS
)
async def list_formats(client, message):
    status_message = "**Status:**\n\n"
    status_message += "Cookies: Checking...\nAuth Token: Checking..."
    status_msg = await message.reply_text(status_message)

    cookie_status = await check_cookies("https://www.youtube.com/watch?v=LLF3GMfNEYU")
    status_message = "**Status:**\n\n"
    status_message += f"Cookies: {'✅ Alive' if cookie_status else '❌ Dead'}\nAuth Token: Checking..."
    await status_msg.edit_text(status_message)

    use_token = await check_auth_token()
    status_message = "**Status:**\n\n"
    status_message += f"Cookies: {'✅ Alive' if cookie_status else '❌ Dead'}\n"
    status_message += f"Auth Token: {'✅ Alive' if use_token else '❌ Dead'}"
    await status_msg.edit_text(status_message)

    if not use_token:
        status_message += "\n\n**Generating a new Auth token...**"
        await status_msg.edit_text(status_message)
        try:
            generate_new_auth_token()  # Generate and update the new token
            await message.reply_text(f"\n**✅ Successfully generated and updated a new token.**")
        except Exception as ex:
            logger.error(f"Failed to generate a new token: {ex}")
            await message.reply_text(
                f"\n**❌ Failed to generate a new token: {str(ex)}**"
            )

def check_cookies_expiry():
    if not os.path.exists(COOKIES_FILE):
        logger.error("Cookies file not found.")
        return False

    with open(COOKIES_FILE, "r") as file:
        cookies = file.read()
        if "expires" in cookies:
            expiry_time = float(cookies.split("expires=")[1].split(";")[0])
            if time.time() > expiry_time:
                logger.info("Cookies have expired.")
                return False
            else:
                logger.info("Cookies are still valid.")
                return True
        else:
            logger.error("No expiry information found in cookies.")
            return False

def generate_new_cookies():
    # Placeholder for generating new cookies
    # This should be replaced with actual logic to generate new cookies
    new_cookies = "new_cookies_data_here"
    with open(COOKIES_FILE, "w") as file:
        file.write(new_cookies)
    logger.info("New cookies generated and saved.")

def replace_cookies_if_expired():
    if not check_cookies_expiry():
        generate_new_cookies()

# Example usage
if __name__ == "__main__":
    TheChampu()
    replace_cookies_if_expired()