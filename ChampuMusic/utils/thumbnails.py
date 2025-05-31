import os
import re
import random
import aiohttp
import aiofiles
import traceback

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from youtubesearchpython.__future__ import VideosSearch

def changeImageSize(maxWidth, maxHeight, image):
    ratio = min(maxWidth / image.size[0], maxHeight / image.size[1])
    newSize = (int(image.size[0] * ratio), int(image.size[1] * ratio))
    return image.resize(newSize, Image.ANTIALIAS)

def truncate_ellipsis(text, max_chars=20):
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    if ' ' in truncated:
        truncated = truncated[:truncated.rfind(' ')]
    return truncated + "..." if len(truncated) > 0 else text[:max_chars-3] + "..."

def ensure_text_fits(draw, text, font, max_width):
    """Ensure text doesn't exceed max width by truncating with ellipsis"""
    text_width = draw.textlength(text, font=font)
    if text_width <= max_width:
        return text
    
    # Binary search for optimal truncation
    low = 1
    high = len(text)
    best = ""
    while low <= high:
        mid = (low + high) // 2
        truncated = truncate_ellipsis(text, mid)
        truncated_width = draw.textlength(truncated, font=font)
        if truncated_width <= max_width:
            best = truncated
            low = mid + 1
        else:
            high = mid - 1
    return best if best else "..."

def fit_text(draw, text, max_width, font_path, start_size, min_size):
    size = start_size
    while size >= min_size:
        font = ImageFont.truetype(font_path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 1
    return ImageFont.truetype(font_path, min_size)

async def get_thumb(videoid: str):
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        result = (await results.next())["result"][0]

        title = result.get("title", "Unknown Title")
        duration = result.get("duration", "00:00")
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        channel = result.get("channel", {}).get("name", "Unknown Channel")

        # Download thumbnail
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(f"cache/thumb{videoid}.png", mode="wb") as f:
                        await f.write(await resp.read())

        base_img = Image.open(f"cache/thumb{videoid}.png").convert("RGBA")
        bg_img = changeImageSize(1280, 720, base_img).convert("RGBA")
        blurred_bg = bg_img.filter(ImageFilter.GaussianBlur(30))



        # Card overlay
        card_width, card_height = 960, 320  # <-- Add this line
        card = Image.new("RGBA", (card_width, card_height), (40, 40, 60, 200))
        mask = Image.new("L", (card_width, card_height), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([0, 0, card_width, card_height], radius=40, fill=255)
        card_pos = ((1280 - card_width) // 2, (720 - card_height) // 2)
        blurred_bg.paste(card, card_pos, mask)
        
        final_bg = blurred_bg.copy()
        final_bg.paste(card, card_pos, mask)
        draw = ImageDraw.Draw(final_bg)


        # Font paths
        font_path_regular = "ChampuMusic/assets/font2.ttf"
        font_path_bold = "ChampuMusic/assets/font3.ttf"

        # Medium album art 
        thumb_size = 250
        corner_radius = 40
        mask = Image.new('L', (thumb_size, thumb_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle((0, 0, thumb_size, thumb_size), radius=corner_radius, fill=255)

        thumb_square = base_img.resize((thumb_size, thumb_size))
        thumb_square.putalpha(mask)

        thumb_x = card_pos[0] + 40
        thumb_y = card_pos[1] + (card_height - thumb_size) // 2
        final_bg.paste(thumb_square, (thumb_x, thumb_y), thumb_square)

        # Text layout with overflow protection
        text_x = thumb_x + thumb_size + 40
        text_y = thumb_y + 20
        max_text_width = card_width - (text_x - card_pos[0]) - 40

        # Fonts
        font_small = ImageFont.truetype(font_path_regular, 28)
        font_medium = ImageFont.truetype(font_path_regular, 36)
        font_title = fit_text(draw, title, max_text_width, font_path_bold, 48, 32)

        # Channel name (with overflow protection)
        channel_text = ensure_text_fits(draw, channel, font_small, max_text_width)
        draw.text((text_x, text_y), "NOW PLAYING", fill=(180, 180, 180), font=font_small)
        
        # Title (with dynamic sizing and overflow protection)
        title_text = ensure_text_fits(draw, title, font_title, max_text_width)
        draw.text(
            (text_x, text_y + 40),
            title_text,
            fill=(255, 255, 255),
            font=font_title
        )
        
        # Artist and duration
        artist_text = ensure_text_fits(draw, channel, font_medium, max_text_width)
        draw.text((text_x, text_y + 100), artist_text, fill=(200, 200, 200), font=font_medium)
        
        duration_text = f"00:00 / {duration}"
        duration_text = ensure_text_fits(draw, duration_text, font_small, max_text_width)
        draw.text((text_x, text_y + 150), duration_text, fill=(170, 170, 170), font=font_small)

        output_path = f"cache/{videoid}_styled.png"
        final_bg.save(output_path)

        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass

        return output_path

    except Exception as e:
        print(f"[get_thumb Error] {e}")
        traceback.print_exc()
        return None