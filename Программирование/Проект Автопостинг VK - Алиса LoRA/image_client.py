"""
Image generation client — generates unique photographic scenes for each slide.
Uses character DNA from character.py and guarantees dynamic per-slide variations.
"""

from __future__ import annotations

import io
import logging
import random
import urllib.parse
import ssl
import aiohttp

from config import get_settings
from character import build_character_prompt

logger = logging.getLogger(__name__)


async def _generate_flux_direct(prompt: str, width: int, height: int) -> io.BytesIO:
    """Generate image via high-resolution FLUX with unique random seed per slide."""
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Dynamic seed ensures EVERY slide has its own unique scene, pose, and angle
    seed = random.randint(100000, 99999999)
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true&seed={seed}"

    connector = aiohttp.TCPConnector(ssl=ssl_context)
    timeout = aiohttp.ClientTimeout(total=90)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
            resp.raise_for_status()
            data = await resp.read()
            logger.info("Direct FLUX image generated (%d bytes, seed=%d)", len(data), seed)
            buf = io.BytesIO(data)
            buf.seek(0)
            return buf


async def generate_slide_image(scene_description: str, character_outfit: str) -> io.BytesIO:
    """
    Generate an authentic photographic scene for a slide.
    Combines character DNA + chosen outfit + specific scene action.
    """
    settings = get_settings()
    full_prompt = build_character_prompt(scene_description, character_outfit)
    logger.info("Generating slide prompt (truncated): %s", full_prompt[:140])

    # If Fal.ai key is funded, try Fal.ai first
    if settings.image_api_key and "ВСТАВЬТЕ" not in settings.image_api_key:
        try:
            headers = {
                "Authorization": f"Key {settings.image_api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "prompt": full_prompt,
                "image_size": {
                    "width": settings.card_width,
                    "height": settings.card_height,
                },
                "num_images": 1,
            }
            submit_url = f"https://fal.run/{settings.image_model}"

            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            connector = aiohttp.TCPConnector(ssl=ssl_context)

            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=120)) as session:
                async with session.post(submit_url, json=payload, headers=headers) as resp:
                    if resp.status == 200:
                        body = await resp.json()
                        img_url = body.get("images", [{}])[0].get("url")
                        if img_url:
                            async with session.get(img_url) as img_resp:
                                img_resp.raise_for_status()
                                data = await img_resp.read()
                                buf = io.BytesIO(data)
                                buf.seek(0)
                                return buf
                    else:
                        logger.warning("Fal.ai returned %d. Using direct FLUX engine...", resp.status)
        except Exception as e:
            logger.warning("Fal.ai failed: %s. Using direct FLUX engine...", e)

    return await _generate_flux_direct(full_prompt, settings.card_width, settings.card_height)
