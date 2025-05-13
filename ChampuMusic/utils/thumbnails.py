import os
from pathlib import Path
from typing import Dict, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pkg_resources import ensure_directory

# Constants
CACHE_DIR = "cache"
ASSETS_DIR = "ChampuMusic/assets"
THUMBNAIL_SIZE = (1280, 720)
CARD_WIDTH, CARD_HEIGHT = 900, 240
THUMB_SIZE = 180
CARD_CORNER_RADIUS = 40
THUMB_CORNER_RADIUS = 24
PROGRESS_BAR_RADIUS = 4
DEFAULT_THUMBNAIL_URL = "https://i.ytimg.com/vi/{videoid}/hqdefault.jpg"

# Color scheme - Translucent grey theme
COLORS = {
    "background_darken": 0.6,
    "card_bg": (50, 50, 50, 180),
    "label_text": (220, 220, 220, 255),
    "title_text": (255, 255, 255, 255),
    "subtitle_text": (200, 200, 200, 255),
    "progress_bg": (80, 80, 80, 150),
    "progress_fg": (255, 255, 255, 255),
    "drop_shadow": (0, 0, 0, 100)
}

# Font sizes
FONT_SIZES = {
    "title": 36,
    "subtitle": 24,
    "label": 18
}

class ThumbnailGenerator:
    def __init__(self):
        self._fonts_loaded = False
        self._fonts = {}

    def _load_fonts(self) -> None:
        """Load all required fonts."""
        if self._fonts_loaded:
            return

        try:
            self._fonts = {
                "title": self._load_font("font3.ttf", FONT_SIZES["title"]),
                "subtitle": self._load_font("font2.ttf", FONT_SIZES["subtitle"]),
                "label": self._load_font("font.ttf", FONT_SIZES["label"])
            }
            self._fonts_loaded = True
        except Exception as e:
            print(f"Error loading fonts: {e}")
            self._load_fallback_fonts()

    def _load_fallback_fonts(self) -> None:
        """Load fallback fonts if primary fonts fail."""
        default_font = ImageFont.load_default()
        self._fonts = {
            "title": default_font,
            "subtitle": default_font,
            "label": default_font
        }
        self._fonts_loaded = True

    def _load_font(self, font_name: str, size: int) -> ImageFont.FreeTypeFont:
        """Load a specific font with error handling."""
        font_path = Path(ASSETS_DIR) / font_name
        if font_path.exists():
            try:
                return ImageFont.truetype(str(font_path), size)
            except Exception as e:
                print(f"Error loading font {font_name}: {e}")
        return ImageFont.load_default()

    @staticmethod
    def add_rounded_corners(image: Image.Image, radius: int) -> Image.Image:
        """Add rounded corners to an image with transparency."""
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, *image.size), radius, fill=255)
        image.putalpha(mask)
        return image

    @staticmethod
    def truncate_text(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont, 
                     max_width: int, ellipsis: str = "...") -> str:
        """Truncate text with ellipsis if it exceeds max width using binary search."""
        if draw.textlength(text, font=font) <= max_width:
            return text

        low, high = 0, len(text)
        while low <= high:
            mid = (low + high) // 2
            truncated = text[:mid] + ellipsis
            text_width = draw.textlength(truncated, font=font)
            
            if text_width <= max_width:
                low = mid + 1
            else:
                high = mid - 1

        return text[:high] + ellipsis if high > 0 else ellipsis

    @staticmethod
    def create_progress_bar(draw: ImageDraw.Draw, position: Tuple[int, int], 
                           size: Tuple[int, int], progress: float) -> None:
        """Draw a progress bar with rounded corners."""
        x, y = position
        width, height = size
        
        # Draw background
        draw.rounded_rectangle(
            (x, y, x + width, y + height),
            radius=PROGRESS_BAR_RADIUS,
            fill=COLORS["progress_bg"]
        )
        
        # Draw progress
        progress_width = max(0, min(width, int(width * progress)))
        if progress_width > 0:
            draw.rounded_rectangle(
                (x, y, x + progress_width, y + height),
                radius=PROGRESS_BAR_RADIUS,
                fill=COLORS["progress_fg"]
            )

    async def create_modern_thumbnail(self, videoid: str, video_info: Dict) -> Optional[str]:
        """Create a modern translucent player card thumbnail."""
        try:
            cache_path = Path(CACHE_DIR)
            cache_path.mkdir(exist_ok=True)
            cache_file = cache_path / f"{videoid}_v5.png"

            if cache_file.exists():
                return str(cache_file)

            temp_path = cache_path / f"thumb{videoid}.png"
            if not await self.download_thumbnail(video_info.get("thumbnail"), temp_path):
                return None

            with Image.open(temp_path) as thumb:
                # Create blurred background
                bg = thumb.resize(THUMBNAIL_SIZE).filter(ImageFilter.GaussianBlur(radius=18))
                bg = ImageEnhance.Brightness(bg).enhance(COLORS["background_darken"])

                # Create player card
                card = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), (0, 0, 0, 0))
                card_draw = ImageDraw.Draw(card)

                # Draw shadow and card
                card_draw.rounded_rectangle(
                    (5, 5, CARD_WIDTH - 5, CARD_HEIGHT - 5),
                    radius=CARD_CORNER_RADIUS,
                    fill=COLORS["drop_shadow"]
                )
                card_draw.rounded_rectangle(
                    (0, 0, CARD_WIDTH, CARD_HEIGHT),
                    radius=CARD_CORNER_RADIUS,
                    fill=COLORS["card_bg"]
                )

                # Add album thumbnail
                album_thumb = thumb.copy().resize((THUMB_SIZE, THUMB_SIZE))
                album_thumb = self.add_rounded_corners(album_thumb, THUMB_CORNER_RADIUS)
                card.paste(album_thumb, (30, 30), album_thumb)

                # Load fonts if not already loaded
                self._load_fonts()

                # Draw text elements with proper spacing
                text_x = 230
                channel = video_info.get("channel", "Unknown Channel")
                title = video_info.get("title", "Unknown Title")
                artist = video_info.get("artist", "Unknown Artist")

                # Channel name (top)
                card_draw.text(
                    (text_x, 30), 
                    channel, 
                    font=self._fonts["label"], 
                    fill=COLORS["label_text"]
                )

                # Title (middle)
                truncated_title = self.truncate_text(
                    card_draw, title, self._fonts["title"], CARD_WIDTH - 260
                )
                card_draw.text(
                    (text_x, 70), 
                    truncated_title, 
                    font=self._fonts["title"], 
                    fill=COLORS["title_text"]
                )

                # Artist (bottom)
                card_draw.text(
                    (text_x, 130), 
                    artist, 
                    font=self._fonts["subtitle"], 
                    fill=COLORS["subtitle_text"]
                )

                # Progress bar
                self.create_progress_bar(
                    card_draw,
                    (text_x, 190),
                    (620, 8),
                    0.24  # Default progress
                )

                # Combine everything
                final_img = bg.copy()
                card_position = (
                    (THUMBNAIL_SIZE[0] - CARD_WIDTH) // 2,
                    (THUMBNAIL_SIZE[1] - CARD_HEIGHT) // 2
                )
                final_img.paste(card, card_position, card)
                final_img.save(cache_file, quality=95, optimize=True)

            # Cleanup
            try:
                temp_path.unlink()
            except Exception as e:
                print(f"Error cleaning up temp file: {e}")

            return str(cache_file)

        except Exception as e:
            print(f"Error in create_modern_thumbnail: {e}")
            return None

    async def get_thumb(self, videoid: str, modern_style: bool = False) -> str:
        """Main function to get or generate thumbnail."""
        try:
            cache_path = Path(CACHE_DIR)
            cache_path.mkdir(exist_ok=True)
            
            version = "v5" if modern_style else "v4"
            cache_file = cache_path / f"{videoid}_{version}.png"

            if cache_file.exists():
                return str(cache_file)

            video_info = await self.get_video_info(videoid)
            if not video_info:
                return DEFAULT_THUMBNAIL_URL.format(videoid=videoid)

            if modern_style:
                result = await self.create_modern_thumbnail(videoid, video_info)
                return result or DEFAULT_THUMBNAIL_URL.format(videoid=videoid)
            
            # Original thumbnail generation
            temp_path = cache_path / f"thumb{videoid}.png"
            if not await self.download_thumbnail(video_info.get("thumbnail"), temp_path):
                return DEFAULT_THUMBNAIL_URL.format(videoid=videoid)

            if not await self.generate_thumbnail_image(video_info, temp_path, cache_file):
                return DEFAULT_THUMBNAIL_URL.format(videoid=videoid)

            try:
                temp_path.unlink()
            except Exception as e:
                print(f"Error cleaning up temp file: {e}")

            return str(cache_file)

        except Exception as e:
            print(f"Error in get_thumb: {e}")
            return DEFAULT_THUMBNAIL_URL.format(videoid=videoid)

    async def download_thumbnail(self, url: str, save_path: Path) -> bool:
        """Download thumbnail from URL."""
        # Implementation would go here
        pass

    async def get_video_info(self, videoid: str) -> Dict:
        """Get video information."""
        # Implementation would go here
        pass

    async def generate_thumbnail_image(self, video_info: Dict, 
                                     temp_path: Path, cache_file: Path) -> bool:
        """Generate original style thumbnail."""
        # Implementation would go here
        pass