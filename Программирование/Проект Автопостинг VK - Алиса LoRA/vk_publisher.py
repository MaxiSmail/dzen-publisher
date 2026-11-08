"""
VK Publisher — handles multi-image carousel uploading and publishing to VK wall:
  1. For each image: photos.getWallUploadServer → upload → photos.saveWallPhoto
  2. Combine all photo IDs into comma-separated attachments
  3. wall.post(attachments="photoX_Y,photoX_Z...", message=caption)
"""

from __future__ import annotations

import asyncio
import io
import logging
from typing import Any

import aiohttp
import requests

from config import get_settings

logger = logging.getLogger(__name__)

VK_API_BASE = "https://api.vk.com/method"
ERR_FLOOD_CONTROL = 9
ERR_CAPTCHA = 14
ERR_TOO_MANY_REQUESTS = 6
FLOOD_BACKOFF_SECONDS = 30
MAX_RETRIES = 3


class VKPublishError(Exception):
    """Raised when VK API returns a non-recoverable error."""


async def _vk_request(
    session: aiohttp.ClientSession,
    method: str,
    params: dict[str, Any],
) -> dict[str, Any]:
    """Execute a VK API method with automatic flood-control retry."""
    settings = get_settings()
    params.setdefault("access_token", settings.vk_access_token)
    params.setdefault("v", settings.vk_api_version)

    url = f"{VK_API_BASE}/{method}"

    for attempt in range(1, MAX_RETRIES + 1):
        async with session.post(url, data=params) as resp:
            body = await resp.json()

        if "error" in body:
            error = body["error"]
            code = error.get("error_code", 0)
            msg = error.get("error_msg", "unknown")

            if code in (ERR_FLOOD_CONTROL, ERR_TOO_MANY_REQUESTS):
                wait = FLOOD_BACKOFF_SECONDS * attempt
                logger.warning(
                    "VK flood control (code %d), backing off %ds (attempt %d/%d)",
                    code, wait, attempt, MAX_RETRIES,
                )
                await asyncio.sleep(wait)
                continue

            if code == ERR_CAPTCHA:
                raise VKPublishError(
                    f"VK requires CAPTCHA: {error.get('captcha_img', 'N/A')}"
                )

            raise VKPublishError(f"VK API error [{code}]: {msg}")

        return body.get("response", body)  # type: ignore[no-any-return]

    raise VKPublishError(f"VK API {method}: max retries exceeded")


async def _upload_single_photo(
    session: aiohttp.ClientSession,
    group_id: int,
    image_bytes: io.BytesIO,
) -> str:
    """Upload one image and return its VK attachment string (e.g. photo123_456)."""
    raw_data = image_bytes.getvalue()
    loop = asyncio.get_running_loop()

    for attempt in range(1, 11):
        try:
            # 1. Get fresh upload URL
            srv = await _vk_request(session, "photos.getWallUploadServer", {"group_id": group_id})
            upload_url = srv["upload_url"]

            # 2. Upload via requests in executor
            def _sync_upload() -> dict[str, Any]:
                files = {
                    "photo": ("photo.jpg", raw_data, "image/jpeg"),
                }
                resp = requests.post(
                    upload_url,
                    files=files,
                    headers={"User-Agent": "Mozilla/5.0"},
                    verify=False,
                    timeout=60,
                )
                return resp.json()  # type: ignore[no-any-return]

            upload_result = await loop.run_in_executor(None, _sync_upload)
            photo_val = upload_result.get("photo")

            if not photo_val or photo_val in ('""', "[]", "null"):
                logger.warning("Upload attempt %d/10: server returned empty photo, retrying in 2.5s...", attempt)
                await asyncio.sleep(2.5)
                continue

            # 3. Save photo
            saved = await _vk_request(session, "photos.saveWallPhoto", {
                "group_id": group_id,
                "photo": upload_result["photo"],
                "server": upload_result["server"],
                "hash": upload_result["hash"],
            })

            if not saved or not isinstance(saved, list):
                raise ValueError(f"Invalid saveWallPhoto response: {saved}")

            photo = saved[0]
            attachment = f"photo{photo['owner_id']}_{photo['id']}"
            return attachment

        except Exception as exc:
            logger.warning("Upload photo attempt %d failed: %s", attempt, exc)
            if attempt == 10:
                raise VKPublishError(f"Failed to upload photo after 10 attempts: {exc}")
            await asyncio.sleep(2.5)

    raise VKPublishError("Photo upload exhausted 10 retries")


async def publish_carousel(
    images_bytes: list[io.BytesIO],
    post_caption: str,
) -> int:
    """
    Upload a list of carousel images to VK and publish them as a single multi-photo wall post.
    """
    settings = get_settings()
    group_id = settings.vk_group_id
    owner_id = -group_id

    import ssl
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    timeout = aiohttp.ClientTimeout(total=300)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        attachments: list[str] = []
        for idx, img_buf in enumerate(images_bytes, start=1):
            logger.info("Uploading carousel slide %d/%d to VK", idx, len(images_bytes))
            att = await _upload_single_photo(session, group_id, img_buf)
            logger.info("Slide %d uploaded: %s", idx, att)
            attachments.append(att)
            await asyncio.sleep(1)

        attachments_str = ",".join(attachments)
        logger.info("Publishing wall post with %d attachments...", len(attachments))

        post_result = await _vk_request(session, "wall.post", {
            "owner_id": owner_id,
            "from_group": 1,
            "message": post_caption,
            "attachments": attachments_str,
        })

        post_id: int = post_result.get("post_id", 0)
        logger.info("VK carousel post published! post_id=%d", post_id)
        return post_id
