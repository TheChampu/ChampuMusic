import os
import re
import asyncio
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL

# Constants
CACHE_DIR = "cache"
ASSETS_DIR = "ChampuMusic/assets"
DEFAULT_FONT_SIZE = 30
TITLE_FONT_SIZE = 45
THUMBNAIL_SIZE = (1280, 720)
CIRCLE_SIZE = 400

def ensure_directories():
    """Ensure required directories exist."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    if not os.path.exists(ASSETS_DIR):
        raise FileNotFoundError(f"Assets directory not found: {ASSETS_DIR}")

def load_font(font_path, size, fallback=True):
    """Safely load font with fallback to default."""
    try:
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
        if fallback:
            return ImageFont.load_default(size)
        raise FileNotFoundError(f"Font not found: {font_path}")
    except Exception as e:
        print(f"Font loading error: {e}")
        return ImageFont.load_default(size) if fallback else None

def changeImageSize(maxWidth, maxHeight, image):
    """Resize image with safety checks."""
    if not image:
        raise ValueError("No image provided for resizing")
    try:
        widthRatio = maxWidth / image.size[0]
        heightRatio = maxHeight / image.size[1]
        newWidth = int(widthRatio * image.size[0])
        newHeight = int(heightRatio * image.size[1])
        return image.resize((newWidth, newHeight))
    except Exception as e:
        print(f"Image resize error: {e}")
        return image  # Return original if resize fails

def truncate(text):
    """Safe text truncation with type checking."""
    if not isinstance(text, str):
        text = str(text)
    
    text = re.sub(r"\W+", " ", text).strip()
    parts = []
    current = ""
    
    for word in text.split():
        if len(current) + len(word) < 30:
            current += " " + word if current else word
        else:
            parts.append(current)
            current = word
    if current:
        parts.append(current)
    
    return parts[:2] if len(parts) > 1 else [parts[0], ""] if parts else ["", ""]

def crop_center_circle(img, output_size, border, crop_scale=1.5):
    """Safe circular cropping with error handling."""
    if not img:
        raise ValueError("No image provided for cropping")
    
    try:
        half_width = img.size[0] / 2
        half_height = img.size[1] / 2
        larger_size = int(output_size * crop_scale)
        
        img = img.crop((
            half_width - larger_size/2,
            half_height - larger_size/2,
            half_width + larger_size/2,
            half_height + larger_size/2
        ))
        
        img = img.resize((output_size - 2*border, output_size - 2*border))
        
        final_img = Image.new("RGBA", (output_size, output_size), "white")
        mask_main = Image.new("L", (output_size - 2*border, output_size - 2*border), 0)
        draw_main = ImageDraw.Draw(mask_main)
        draw_main.ellipse((0, 0, output_size - 2*border, output_size - 2*border), fill=255)
        
        final_img.paste(img, (border, border), mask_main)
        
        mask_border = Image.new("L", (output_size, output_size), 0)
        draw_border = ImageDraw.Draw(mask_border)
        draw_border.ellipse((0, 0, output_size, output_size), fill=255)
        
        return Image.composite(final_img, Image.new("RGBA", final_img.size, (0, 0, 0, 0)), mask_border)
    except Exception as e:
        print(f"Circle crop error: {e}")
        return img  # Return original if crop fails

async def download_thumbnail(url, save_path, retries=3):
    """Download thumbnail with retries and timeout."""
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(save_path, "wb") as f:
                            await f.write(await resp.read())
                        return True
                    print(f"Download failed (attempt {attempt + 1}): HTTP {resp.status}")
        except Exception as e:
            print(f"Download error (attempt {attempt + 1}): {str(e)}")
        await asyncio.sleep(1)
    return False

async def get_video_info(videoid):
    """Get video info with comprehensive error handling."""
    try:
        results = await VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1).next()
        if not results or not results.get("result"):
            raise ValueError("No results found")
        
        video = results["result"][0]
        return {
            "title": str(video.get("title", "Unsupported Title")),
            "duration": str(video.get("duration", "Unknown")),
            "thumbnail": video["thumbnails"][0]["url"].split("?")[0],
            "views": str(video.get("viewCount", {}).get("short", "Unknown")),
            "channel": str(video.get("channel", {}).get("name", "Unknown"))
        }
    except Exception as e:
        print(f"Video info error: {e}")
        return None

async def generate_thumbnail_image(video_info, temp_path, output_path):
    """Generate the final thumbnail image."""
    try:
        # Load downloaded thumbnail
        with Image.open(temp_path) as youtube:
            # Create base image
            image1 = changeImageSize(*THUMBNAIL_SIZE, youtube)
            image2 = image1.convert("RGBA")
            background = image2.filter(filter=ImageFilter.BoxBlur(20))
            enhancer = ImageEnhance.Brightness(background)
            background = enhancer.enhance(0.6)
            draw = ImageDraw.Draw(background)

            # Load fonts with fallbacks
            arial = load_font(f"{ASSETS_DIR}/font2.ttf", DEFAULT_FONT_SIZE)
            font = load_font(f"{ASSETS_DIR}/font.ttf", DEFAULT_FONT_SIZE)
            title_font = load_font(f"{ASSETS_DIR}/font3.ttf", TITLE_FONT_SIZE)

            # Add circular thumbnail
            circle_thumbnail = crop_center_circle(youtube, CIRCLE_SIZE, 20)
            if circle_thumbnail:
                circle_thumbnail = circle_thumbnail.resize((CIRCLE_SIZE, CIRCLE_SIZE))
                background.paste(circle_thumbnail, (120, 160), circle_thumbnail)

            # Add text elements
            text_x = 565
            title_parts = truncate(video_info["title"])
            draw.text((text_x, 180), title_parts[0], fill="white", font=title_font)
            draw.text((text_x, 230), title_parts[1], fill="white", font=title_font)
            
            info_text = f"{video_info['channel']}  |  {video_info['views'][:23]}"
            draw.text((text_x, 320), info_text, fill="white", font=arial)

            # Add progress bar
            line_length = 580
            red_length = int(line_length * 0.6)
            draw.line([(text_x, 380), (text_x + red_length, 380)], fill="red", width=9)
            draw.line([(text_x + red_length, 380), (text_x + line_length, 380)], fill="white", width=8)
            
            # Add progress circle
            circle_radius = 10
            draw.ellipse([
                text_x + red_length - circle_radius,
                380 - circle_radius,
                text_x + red_length + circle_radius,
                380 + circle_radius
            ], fill="red")

            # Add time text
            draw.text((text_x, 400), "00:00", fill="white", font=arial)
            draw.text((1080, 400), video_info["duration"], fill="white", font=arial)

            # Add play icons if available
            play_icons_path = f"{ASSETS_DIR}/play_icons.png"
            if os.path.exists(play_icons_path):
                try:
                    with Image.open(play_icons_path) as play_icons:
                        play_icons = play_icons.resize((580, 62))
                        background.paste(play_icons, (text_x, 450), play_icons)
                except Exception as e:
                    print(f"Play icons error: {e}")

            # Save final image
            background.save(output_path)
            return True
    except Exception as e:
        print(f"Thumbnail generation error: {e}")
        return False

async def get_thumb(videoid):
    """Main function to get or generate thumbnail."""
    try:
        ensure_directories()
        cache_file = f"{CACHE_DIR}/{videoid}_v4.png"
        
        # Return cached version if available
        if os.path.exists(cache_file):
            return cache_file

        # Get video info
        video_info = await get_video_info(videoid)
        if not video_info:
            return YOUTUBE_IMG_URL

        # Download thumbnail
        temp_path = f"{CACHE_DIR}/thumb{videoid}.png"
        if not await download_thumbnail(video_info["thumbnail"], temp_path):
            return YOUTUBE_IMG_URL

        # Generate final thumbnail
        if not await generate_thumbnail_image(video_info, temp_path, cache_file):
            return YOUTUBE_IMG_URL

        # Cleanup temp file
        try:
            os.remove(temp_path)
        except:
            pass

        return cache_file

    except Exception as e:
        print(f"Error in get_thumb: {e}")
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
