"""
Renderer — assembles comic-style story cards and covers using Pillow.
Supports:
  1. Cover Slide: White top header with bold title (accent word in red) + red card frame.
  2. Story Slide: Full photo + comic speech bubble with pointer tail and bold typography.
"""

from __future__ import annotations

import io
import logging
import math
import textwrap
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

from config import get_settings

logger = logging.getLogger(__name__)

FRAME_COLOR = (230, 20, 20)          # Punchy red border frame
FRAME_WIDTH = 22                      # px
HEADER_BG = (255, 255, 255)          # White header box
HEADER_TEXT_BLACK = (15, 15, 15)     # Deep black for header text
HEADER_TEXT_RED = (230, 20, 20)       # Accent red word
BUBBLE_BG = (255, 255, 255)          # Comic bubble background
BUBBLE_BORDER = (220, 20, 20)        # Comic bubble red outline
BUBBLE_TEXT_COLOR = (10, 10, 10)     # Bubble text color


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    """Load Montserrat-Bold font."""
    settings = get_settings()
    try:
        return ImageFont.truetype(str(settings.default_font_path), size)
    except OSError:
        return ImageFont.load_default()


def _crop_and_resize(image: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Center-crop and resize image to exact target dimensions."""
    bg = image.convert("RGB")
    bg_ratio = bg.width / bg.height
    target_ratio = target_w / target_h

    if bg_ratio > target_ratio:
        new_w = int(bg.height * target_ratio)
        left = (bg.width - new_w) // 2
        bg = bg.crop((left, 0, left + new_w, bg.height))
    else:
        new_h = int(bg.width / target_ratio)
        top = (bg.height - new_h) // 2
        bg = bg.crop((0, top, bg.width, top + new_h))

    return bg.resize((target_w, target_h), Image.LANCZOS)


def render_cover_slide(
    background_bytes: io.BytesIO,
    cover_header: str,
    accent_word: str,
) -> io.BytesIO:
    """
    Render Slide 1:
    - Red border around the entire card.
    - White top box with bold title, coloring the `accent_word` in vibrant red.
    - Photo fills the rest of the canvas.
    """
    settings = get_settings()
    target_w, target_h = settings.card_width, settings.card_height

    background_bytes.seek(0)
    bg = Image.open(background_bytes)
    base_img = _crop_and_resize(bg, target_w, target_h)

    # 1. Calculate header area
    header_height = int(target_h * 0.26)
    card = Image.new("RGB", (target_w, target_h), HEADER_BG)

    # Paste photo in the bottom area (from header_height down to bottom)
    photo_h = target_h - header_height
    photo_cropped = _crop_and_resize(bg, target_w, photo_h)
    card.paste(photo_cropped, (0, header_height))

    draw = ImageDraw.Draw(card)

    # 2. Render Header Text
    # Split text into words and identify accent word
    clean_header = cover_header.strip()
    words = clean_header.split()
    accent_clean = accent_word.strip().lower().strip(".,!?:;\"'")

    # Choose best font size
    max_w = target_w - (FRAME_WIDTH * 2 + 50)
    max_h = header_height - (FRAME_WIDTH + 30)

    chosen_font = _load_font(52)
    chosen_lines: list[list[str]] = []

    for f_size in range(62, 36, -3):
        font = _load_font(f_size)
        # Line wrap words
        lines: list[list[str]] = []
        current_line: list[str] = []
        current_w = 0
        space_w = font.getlength(" ")

        for w in words:
            w_len = font.getlength(w)
            if not current_line:
                current_line.append(w)
                current_w = w_len
            elif current_w + space_w + w_len <= max_w:
                current_line.append(w)
                current_w += space_w + w_len
            else:
                lines.append(current_line)
                current_line = [w]
                current_w = w_len
        if current_line:
            lines.append(current_line)

        line_h = draw.textbbox((0, 0), "Aq", font=font)[3] + 12
        total_h = len(lines) * line_h
        if total_h <= max_h:
            chosen_font = font
            chosen_lines = lines
            break

    if not chosen_lines:
        chosen_lines = [[w for w in words]]

    # Draw lines centered horizontally and vertically in header
    line_h = draw.textbbox((0, 0), "Aq", font=chosen_font)[3] + 10
    total_h = len(chosen_lines) * line_h
    start_y = FRAME_WIDTH + (header_height - FRAME_WIDTH - total_h) // 2

    space_w = chosen_font.getlength(" ")

    for row_idx, line_words in enumerate(chosen_lines):
        line_w = sum(chosen_font.getlength(w) for w in line_words) + space_w * (len(line_words) - 1)
        cur_x = (target_w - line_w) // 2
        cur_y = start_y + row_idx * line_h

        for w in line_words:
            w_clean = w.lower().strip(".,!?:;\"'")
            color = HEADER_TEXT_RED if w_clean == accent_clean else HEADER_TEXT_BLACK
            draw.text((cur_x, cur_y), w, font=chosen_font, fill=color)
            cur_x += chosen_font.getlength(w) + space_w

    # 3. Draw Outer Red Border
    draw.rectangle([0, 0, target_w - 1, target_h - 1], outline=FRAME_COLOR, width=FRAME_WIDTH)

    # Output JPEG
    output = io.BytesIO()
    card.save(output, format="JPEG", quality=95, optimize=True)
    output.seek(0)
    return output


def _draw_speech_bubble(
    image: Image.Image,
    text: str,
    position: str = "top-left",
) -> Image.Image:
    """Draw an elliptical comic speech bubble with a pointer tail."""
    width, height = image.size
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_size = 38
    font = _load_font(font_size)

    # Word wrap text for bubble
    max_bubble_w = int(width * 0.58)
    avg_char_w = font.getlength("А")
    chars_per_line = max(1, int((max_bubble_w - 60) / avg_char_w))
    lines = textwrap.wrap(text, width=chars_per_line)

    line_h = draw.textbbox((0, 0), "Aq", font=font)[3] + 8
    text_block_h = len(lines) * line_h
    max_line_w = max((draw.textlength(l, font=font) for l in lines), default=100)

    padding_x = 44
    padding_y = 30
    bubble_w = int(max_line_w + padding_x * 2)
    bubble_h = int(text_block_h + padding_y * 2)

    # Determine bubble position
    if "right" in position:
        bx1 = width - bubble_w - 60
        bx2 = width - 60
        tail_tip = (bx1 - 50, int(bubble_h * 1.25))
    else:  # left or center
        bx1 = 60
        bx2 = 60 + bubble_w
        tail_tip = (bx2 + 50, int(bubble_h * 1.25))

    by1 = 70
    by2 = by1 + bubble_h

    # Draw pointer tail (polygon)
    tail_base1 = (bx1 + bubble_w * 0.5, by2 - 10)
    tail_base2 = (bx1 + bubble_w * 0.7, by2 - 10)
    if "right" in position:
        tail_base1 = (bx1 + bubble_w * 0.3, by2 - 10)
        tail_base2 = (bx1 + bubble_w * 0.5, by2 - 10)

    # Draw tail with border
    border_w = 6
    draw.polygon([tail_base1, tail_base2, tail_tip], fill=BUBBLE_BORDER)
    # Inner tail
    inner_base1 = (tail_base1[0], tail_base1[1] - 4)
    inner_base2 = (tail_base2[0], tail_base2[1] - 4)
    draw.polygon([inner_base1, inner_base2, (tail_tip[0], tail_tip[1] - 4)], fill=BUBBLE_BG)

    # Draw bubble ellipse/rounded rectangle
    draw.ellipse([bx1, by1, bx2, by2], fill=BUBBLE_BG, outline=BUBBLE_BORDER, width=border_w)

    # Draw centered text lines inside bubble
    text_start_y = by1 + padding_y
    for i, line in enumerate(lines):
        lw = draw.textlength(line, font=font)
        tx = bx1 + (bubble_w - lw) / 2
        ty = text_start_y + i * line_h
        draw.text((tx, ty), line, font=font, fill=BUBBLE_TEXT_COLOR)

    # Composite with base image
    result = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    return result


def render_story_slide(
    background_bytes: io.BytesIO,
    bubble_text: Optional[str] = None,
    bubble_position: Optional[str] = "top-left",
) -> io.BytesIO:
    """
    Render Story Slide (Slide 2..N):
    - Full-sized visual scene.
    - Comic speech bubble with text and pointer tail.
    - Outer red border frame for visual continuity.
    """
    settings = get_settings()
    target_w, target_h = settings.card_width, settings.card_height

    background_bytes.seek(0)
    bg = Image.open(background_bytes)
    base_img = _crop_and_resize(bg, target_w, target_h)

    # Draw speech bubble if text is provided
    if bubble_text:
        base_img = _draw_speech_bubble(base_img, bubble_text, bubble_position or "top-left")

    # Outer Red Border
    draw = ImageDraw.Draw(base_img)
    draw.rectangle([0, 0, target_w - 1, target_h - 1], outline=FRAME_COLOR, width=FRAME_WIDTH)

    output = io.BytesIO()
    base_img.save(output, format="JPEG", quality=95, optimize=True)
    output.seek(0)
    return output
