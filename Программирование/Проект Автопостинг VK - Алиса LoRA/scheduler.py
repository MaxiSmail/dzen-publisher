"""
Scheduler — orchestrates the full multi-slide carousel pipeline:
  1. DB Check (recent topics)
  2. LLM Story Generation (outfit + cover + story slides with comic bubbles)
  3. Image Generation for each slide (with consistent character and outfit)
  4. Pillow Rendering (Cover Slide header & Story Slide comic speech bubbles)
  5. VK Multi-photo Carousel Upload & Wall Post
  6. DB Log
"""

from __future__ import annotations

import asyncio
import io
import logging
import traceback

from config import get_settings
from database import get_recent_topics, is_topic_exists, save_post
from llm_client import generate_carousel_story
from image_client import generate_slide_image
from renderer import render_cover_slide, render_story_slide
from vk_publisher import publish_carousel

logger = logging.getLogger(__name__)


async def run_pipeline() -> None:
    """
    Execute a single carousel publish cycle end-to-end.
    """
    logger.info("═══ Carousel Pipeline started ═══")

    # ── Step 1: Deduplication topics ────────────────────────
    logger.info("Step 1/6: Loading recent topics from DB")
    recent_topics = await get_recent_topics(limit=50)

    # ── Step 2: Generate Story with Gemini ──────────────────
    logger.info("Step 2/6: Generating carousel story via LLM")
    story = await generate_carousel_story(exclude_topics=recent_topics)
    logger.info(
        "Story generated: topic=%r, outfit=%r, slides=%d",
        story.topic, story.character_outfit, len(story.slides),
    )

    if await is_topic_exists(story.topic):
        logger.warning("Topic %r already exists — regenerating once", story.topic)
        recent_topics.append(story.topic)
        story = await generate_carousel_story(exclude_topics=recent_topics)

    # ── Step 3 & 4: Generate Images and Render Slides ───────
    logger.info("Step 3 & 4: Generating and rendering %d slides...", len(story.slides))
    rendered_slides: list[io.BytesIO] = []

    for idx, slide in enumerate(story.slides, start=1):
        logger.info("Processing slide %d/%d (type=%s)", idx, len(story.slides), slide.slide_type)

        # Generate image for this scene
        raw_img = await generate_slide_image(slide.scene_description, story.character_outfit)

        # Render slide
        if slide.slide_type == "cover" or idx == 1:
            rendered = render_cover_slide(
                background_bytes=raw_img,
                cover_header=story.cover_header,
                accent_word=story.accent_word,
            )
        else:
            rendered = render_story_slide(
                background_bytes=raw_img,
                bubble_text=slide.bubble_text,
                bubble_position=slide.bubble_position or "top-left",
            )

        rendered_slides.append(rendered)
        logger.info("Slide %d/%d rendered successfully", idx, len(story.slides))
        await asyncio.sleep(1)

    # ── Step 5: Publish Carousel to VK ──────────────────────
    logger.info("Step 5/6: Publishing %d slides carousel to VK...", len(rendered_slides))
    vk_post_id = await publish_carousel(
        images_bytes=rendered_slides,
        post_caption=story.post_caption,
    )

    # ── Step 6: Save to database ────────────────────────────
    logger.info("Step 6/6: Saving post to database")
    row_id = await save_post(
        topic=story.topic,
        title=story.cover_header,
        fact_text=story.post_caption[:150],
        image_url=None,
        vk_post_id=vk_post_id,
    )

    logger.info(
        "═══ Carousel Pipeline completed successfully — db_id=%d, vk_post_id=%d ═══",
        row_id, vk_post_id,
    )


async def scheduler_loop() -> None:
    """
    Run the carousel pipeline on a recurring interval.
    """
    settings = get_settings()
    interval_seconds = settings.post_interval_hours * 3600
    logger.info(
        "Scheduler started — posting carousel every %d hours (%d seconds)",
        settings.post_interval_hours, interval_seconds,
    )

    while True:
        try:
            await run_pipeline()
        except Exception:
            logger.error(
                "Carousel pipeline error:\n%s", traceback.format_exc()
            )

        logger.info("Next run in %d hours. Sleeping...", settings.post_interval_hours)
        await asyncio.sleep(interval_seconds)
