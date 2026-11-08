"""
LLM client — generates structured multi-slide carousel stories for VK.
Ensures:
  - Strong, distinct poses and camera angles per slide.
  - Consistent character outfit across all slides of a single story.
  - Punchy comic speech bubbles and engaging VK post caption.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Any

import aiohttp

from config import get_settings

logger = logging.getLogger(__name__)

MAX_RETRIES = 3

SYSTEM_PROMPT = """\
Ты — главный сценарист и визуальный сторителлер для паблика ВКонтакте в формате комикс-историй/каруселей.
Твоя задача — взять интересную историческую, научную или парадоксальную тему и создать захватывающую мини-карусель из 3-4 РАЗНЫХ слайдов.

ГЛАВНАЯ ГЕРОИНЯ (НАБЛЮДАТЕЛЬ-УЧАСТНИК):
- 24-летняя реальная девушка (черные волосы шегги/wolf-cut с челкой, зеленые глаза, естественные веснушки, выразительные живые эмоции).
- Для всей истории ты выбираешь ЕДИНЫЙ наряд (character_outfit), который будет на ней на всех слайдах этой истории (например: "casual red cotton sundress" или "vintage green linen dress" или "simple beige utility jumpsuit").

ВАЖНЕЙШЕЕ ПРАВИЛО КАРУСЕЛИ — РАЗНООБРАЗИЕ КАДРОВ:
Каждый слайд ОБЯЗАН иметь совершенно ДРУГОЙ ракурс, позу и действие героини:
- Слайд 1: Динамичный ракурс (смотрит в подзорную трубу, оглядывается в шоке, указывает рукой на необычный объект).
- Слайд 2: Взаимодействие (сидит рядом с исторической личностью, заглядывает через плечо в документ, спорит, шепчет).
- Слайд 3: Реакция/действие (прячется в окопе, приседает от взрыва, держит старинный компас/прибор, смеется).
- Слайд 4: Кульминация/развязка (указывает на книгу, пожимает плечами, разводит руками с иронией).

СТРУКТУРА JSON:
{
  "topic": "Краткая суть темы (3-5 слов)",
  "cover_header": "Заголовок с интригой (до 7 слов).",
  "accent_word": "акцентное_слово_для_выделения_красным",
  "character_outfit": "casual red ribbed cotton sundress",
  "post_caption": "Подробный увлекательный пост для стены ВК (3-4 абзаца, эмодзи, хештеги, вопрос к подписчикам в конце).",
  "slides": [
    {
      "slide_type": "cover",
      "bubble_text": null,
      "bubble_position": null,
      "scene_description": "wide shot: the girl looking through a vintage brass spyglass with wide surprised eyes, standing next to a 19th-century military officer on a battlefield, a cannonball suspended in midair, smoke and trees in background"
    },
    {
      "slide_type": "story",
      "bubble_text": "Он правда искал ошибки в тексте перед казнью",
      "bubble_position": "top-left",
      "scene_description": "medium close-up shot: the girl sitting on a wooden bench inside a horse carriage, leaning over the shoulder of an 18th-century French noble who is carefully writing on parchment with a quill"
    },
    {
      "slide_type": "story",
      "bubble_text": "Он не успел договорить до конца",
      "bubble_position": "top-right",
      "scene_description": "low angle action shot: the girl crouching low in a muddy dirt trench, holding and shielding a terrified young soldier, dirt and smoke explosion in distance"
    }
  ]
}
"""


@dataclass
class SlideData:
    slide_type: str  # "cover" or "story"
    bubble_text: str | None
    bubble_position: str | None  # "top-left", "top-right", "top-center"
    scene_description: str


@dataclass
class CarouselStory:
    topic: str
    cover_header: str
    accent_word: str
    character_outfit: str
    post_caption: str
    slides: list[SlideData]


def _extract_json(text: str) -> dict[str, Any]:
    cleaned = re.sub(r"```(?:json)?\s*", "", text)
    cleaned = cleaned.strip().rstrip("`")

    try:
        return json.loads(cleaned)  # type: ignore[no-any-return]
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        return json.loads(match.group())  # type: ignore[no-any-return]

    raise ValueError(f"No valid JSON found in LLM response: {text[:200]}")


def _validate_story(data: dict[str, Any]) -> CarouselStory:
    required = ("topic", "cover_header", "accent_word", "character_outfit", "post_caption", "slides")
    missing = [f for f in required if not data.get(f)]
    if missing:
        raise ValueError(f"Missing fields: {missing}")

    raw_slides = data["slides"]
    if not isinstance(raw_slides, list) or len(raw_slides) < 2:
        raise ValueError("At least 2 slides required")

    slides: list[SlideData] = []
    for s in raw_slides:
        slides.append(
            SlideData(
                slide_type=s.get("slide_type", "story"),
                bubble_text=s.get("bubble_text"),
                bubble_position=s.get("bubble_position", "top-left"),
                scene_description=s.get("scene_description", ""),
            )
        )

    return CarouselStory(
        topic=data["topic"].strip(),
        cover_header=data["cover_header"].strip(),
        accent_word=data["accent_word"].strip(),
        character_outfit=data["character_outfit"].strip(),
        post_caption=data["post_caption"].strip(),
        slides=slides,
    )


async def generate_carousel_story(exclude_topics: list[str] | None = None) -> CarouselStory:
    """Call Gemini LLM to generate a full visual carousel story."""
    settings = get_settings()

    topics_block = ""
    if exclude_topics:
        topics_list = "\n".join(f"- {t}" for t in exclude_topics[-30:])
        topics_block = f"\n\nУЖЕ ИСПОЛЬЗОВАННЫЕ ТЕМЫ (НЕ ПОВТОРЯТЬ!):\n{topics_list}"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + topics_block},
        {"role": "user", "content": "Придумай новую захватывающую историю для комикс-карусели из 3-4 слайдов с абсолютно разными ракурсами и действиями героини на каждом слайде."},
    ]

    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.llm_model,
        "messages": messages,
        "temperature": 0.85,
        "max_tokens": 3000,
        "response_format": {"type": "json_object"},
    }

    url = f"{settings.llm_base_url.rstrip('/')}/chat/completions"
    last_error: Exception | None = None

    import ssl
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=connector) as session:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info("LLM Story request attempt %d/%d", attempt, MAX_RETRIES)
                async with session.post(
                    url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=120)
                ) as resp:
                    resp.raise_for_status()
                    body = await resp.json()

                content = body["choices"][0]["message"]["content"]
                data = _extract_json(content)
                story = _validate_story(data)
                logger.info("Generated story: %r with %d slides", story.topic, len(story.slides))
                return story

            except (json.JSONDecodeError, ValueError, KeyError) as exc:
                last_error = exc
                logger.warning("LLM parse error on attempt %d: %s", attempt, exc)
            except (aiohttp.ClientError, asyncio.TimeoutError, TimeoutError, Exception) as exc:
                last_error = exc
                logger.warning("LLM request error on attempt %d: %s", attempt, exc)

    raise RuntimeError(f"Failed to generate story after {MAX_RETRIES} attempts: {last_error}")
