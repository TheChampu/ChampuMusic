import re
import aiohttp
from typing import Union
from youtubesearchpython.__future__ import VideosSearch


class TeraboxAPI:
    def __init__(self):
        # Adjust the regex pattern to match Terabox links correctly
        self.regex = r"^(https:\/\/bj-terabox-video-player\.vercel\.app\/)(.*)$"
        self.base = "https://bj-terabox-video-player.vercel.app/"

    async def valid(self, link: str):
        # Check if the link matches the regex pattern
        return bool(re.match(self.regex, link))

    async def track(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return False
                html = await response.text()
                # Parse the HTML to extract video details
                # You may need to use BeautifulSoup or another parsing library here

        # Assuming you have extracted title, duration, etc.
        title = "Extracted Title"  # Replace with actual extraction logic
        ytlink = "YouTube Link"  # Replace with actual link if needed
        vidid = "Video ID"  # Replace with actual video ID
        duration_min = "Duration"  # Replace with actual duration
        thumbnail = "Thumbnail URL"  # Replace with actual thumbnail URL

        track_details = {
            "title": title,
            "link": ytlink,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details, vidid