import os
import logging
from config import YOUTUBE_IMG_URL
from pkg_resources import ensure_directory
import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from typing import Dict, Optional, Tuple
from youtubesearchpython import VideosSearch

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
ASSETS_DIR = os.path.join("ChampuMusic", "assets")
THUMBNAIL_SIZE = (1280, 720)
CARD_WIDTH, CARD_HEIGHT = 900, 240
THUMB_SIZE = 180
CARD_CORNER_RADIUS = 40
THUMB_CORNER_RADIUS = 24
PROGRESS_BAR_RADIUS = 4


COLORS = {
    "background_darken": 0.5,
    "card_bg": (50, 50, 50, 180),
    "label_text": (220, 220, 220, 255),
    "title_text": "white",
    "subtitle_text": (200, 200, 200, 255),
    "progress_bg": (80, 80, 80, 150),
    "progress_fg": (255, 255, 255, 255),
    "drop_shadow": (0, 0, 0, 100)
}

# Font cache
FONT_CACHE = {}

async def get_video_info(videoid: str) -> Optional[Dict]:
    """Fetch video information using YouTubeSearchPython."""
    try:
        query = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(query, limit=1)
        search_results = await results.next()

        if "result" in search_results and len(search_results["result"]) > 0:
            result = search_results["result"][0]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            return {
                "title": result["title"],
                "channel": result["channel"]["name"],
                "thumbnail": thumbnail
            }
        else:
            logging.error(f"No results found for video ID: {videoid}")
            return None
    except Exception as e:
        logging.error(f"Error in get_video_info: {e}")
        return None

async def download_thumbnail(url: str, save_path: str) -> bool:
    """Download a thumbnail image from a URL and save it to a file."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(save_path, 'wb') as f:
                        f.write(await response.read())
                    return True
                else:
                    logging.error(f"Failed to download thumbnail: {response.status}")
                    return False
    except Exception as e:
        logging.error(f"Error in download_thumbnail: {e}")
        return False

def load_fonts() -> Dict[str, ImageFont.FreeTypeFont]:
    """Load all required fonts with fallback handling."""
    fonts = {
        "title": ("font3.ttf", 36),
        "subtitle": ("font2.ttf", 24),
        "label": ("font.ttf", 18)
    }
    loaded_fonts = {}
    for name, (filename, size) in fonts.items():
        try:
            font_path = os.path.join(ASSETS_DIR, filename)
            if font_path in FONT_CACHE:
                loaded_fonts[name] = FONT_CACHE[font_path]
            else:
                loaded_fonts[name] = ImageFont.truetype(font_path, size)
                FONT_CACHE[font_path] = loaded_fonts[name]
        except Exception as e:
            logging.error(f"⚠️ Couldn't load font {filename}: {e}, using default font.")
            loaded_fonts[name] = ImageFont.load_default()
    return loaded_fonts

def add_rounded_corners(image: Image.Image, radius: int) -> Image.Image:
    """Add rounded corners to an image with transparency."""
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, *image.size), radius, fill=255)
    image.putalpha(mask)
    return image

def truncate_text(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> str:
    """Truncate text with ellipsis if it exceeds max width."""
    ellipsis = "..."
    if draw.textlength(text, font=font) <= max_width:
        return text

    low, high = 1, len(text)
    best = ""
    while low <= high:
        mid = (low + high) // 2
        truncated = text[:mid] + ellipsis
        width = draw.textlength(truncated, font=font)
        if width <= max_width:
            best = truncated
            low = mid + 1
        else:
            high = mid - 1
    return best or ellipsis

def create_progress_bar(draw: ImageDraw.Draw, position: Tuple[int, int], size: Tuple[int, int], progress: float):
    """Draw a progress bar with rounded corners."""
    x, y = position
    width, height = size
    draw.rounded_rectangle(
        (x, y, x + width, y + height),
        radius=PROGRESS_BAR_RADIUS,
        fill=COLORS["progress_bg"]
    )
    progress_width = int(width * progress)
    if progress_width > 0:
        draw.rounded_rectangle(
            (x, y, x + progress_width, y + height),
            radius=PROGRESS_BAR_RADIUS,
            fill=COLORS["progress_fg"]
        )

async def create_thumbnail(videoid: str) -> Optional[str]:
    """Main function to create the thumbnail."""
    try:
        # Ensure cache directory exists
        os.makedirs(exist_ok=True)

        # Fetch video info
        video_info = await get_video_info(videoid)
        if not video_info:
            logging.error("Failed to fetch video info.")
            return None

        # Download thumbnail
        temp_thumbnail_path = os.path.join(f"{videoid}_thumb.jpg")
        if not await download_thumbnail(video_info["thumbnail"], temp_thumbnail_path):
            logging.error("Failed to download thumbnail, using fallback.")
            temp_thumbnail_path = YOUTUBE_IMG_URL

        # Load thumbnail image
        thumb = Image.open(temp_thumbnail_path).convert("RGBA")

        # Create blurred background
        bg = thumb.resize(THUMBNAIL_SIZE).filter(ImageFilter.GaussianBlur(radius=18))
        enhancer = ImageEnhance.Brightness(bg)
        bg = enhancer.enhance(COLORS["background_darken"])

        # Load fonts
        fonts = load_fonts()

        # Create player card
        card = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), (0, 0, 0, 0))
        card_draw = ImageDraw.Draw(card)

        # Draw card background
        card_draw.rounded_rectangle(
            (0, 0, CARD_WIDTH, CARD_HEIGHT),
            radius=CARD_CORNER_RADIUS,
            fill=COLORS["card_bg"]
        )

        # Add album thumbnail
        album_thumb = thumb.copy().resize((THUMB_SIZE, THUMB_SIZE))
        album_thumb = add_rounded_corners(album_thumb, THUMB_CORNER_RADIUS)
        card.paste(album_thumb, (30, 30), album_thumb)

        # Add text
        card_draw.text((230, 30), video_info["channel"], font=fonts["label"], fill=COLORS["label_text"])
        truncated_title = truncate_text(card_draw, video_info["title"], fonts["title"], 620)
        card_draw.text((230, 70), truncated_title, font=fonts["title"], fill=COLORS["title_text"])

        # Combine everything
        final_img = bg.copy()
        card_position = ((THUMBNAIL_SIZE[0] - CARD_WIDTH) // 2, (THUMBNAIL_SIZE[1] - CARD_HEIGHT) // 2)
        final_img.paste(card, card_position, card)

        # Save final image
        output_path = os.path.join(f"{videoid}_final.png")
        final_img.save(output_path, quality=95)
        logging.info(f"✅ Thumbnail successfully saved at: {output_path}")
        return output_path

    except Exception as e:
        logging.error(f"❌ Error creating thumbnail: {e}")
        return None
        return None

async def get_thumb(videoid: str, modern_style: bool = False) -> Optional[str]:
    """Main function to get or generate thumbnail."""
    try:
        ensure_directory(ASSETS_DIR)
        cache_file = os.path.join(f"{videoid}_v5.png" if modern_style else f"{videoid}_v4.png")

        if os.path.exists(cache_file):
            return cache_file

        video_info = await get_video_info(videoid)
        if not video_info:
            return YOUTUBE_IMG_URL

        if modern_style:
            result = await create_thumbnail(videoid, video_info)
            return result or YOUTUBE_IMG_URL
        else:
            temp_path = os.path.join(f"thumb{videoid}.png")
            if not await download_thumbnail(video_info["thumbnail"], temp_path):
                return YOUTUBE_IMG_URL

            if not await create_thumbnail(videoid, video_info):
                return YOUTUBE_IMG_URL

            try:
                os.remove(temp_path)
            except Exception as e:
                logging.warning(f"Failed to delete temp file: {e}")

            return cache_file

    except Exception as e:
        logging.error(f"Error in get_thumb: {e}")
        return YOUTUBE_IMG_URL
    


async def gen_qthumb(vidid):
    try:
        query = f"https://www.youtube.com/watch?v={vidid}"
        results = VideosSearch(query, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail
    except Exception as e:
        return YOUTUBE_IMG_URL