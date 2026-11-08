import json
import time
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List
import config

class VKClipScript(BaseModel):
    title: str
    hook_first_5_sec: str
    voiceover_script: str
    visual_cues: List[str]
    call_to_action: str
    vertical_image_prompt: str
    tags: List[str]

SYSTEM_INSTRUCTION_CLIPS = """Ты — креативный продюсер VK Клипов, YouTube Shorts и Reels канала "НейроСети 2026".
Твоя задача — превратить интересную ИИ-новость или промпт-лайфхак в динамичный сценарий короткого вертикального видео (9:16) на 15-30 секунд.

Структура сценария VK Клипа:
1. HOOK (0-5 сек): Крючок внимания, вызывающий любопытство (например: "Эту нейросеть забанят через неделю, но вот что она умеет...").
2. СУТЬ И ЛАЙФХАК (5-20 сек): Четкая демонстрация фичи, промпта или инструмента.
3. CALL-TO-ACTION (20-25 сек): Призыв подписаться на Telegram-канал за готовым промптом.
4. ИЛЛЮСТРАЦИЯ (9:16): В поле vertical_image_prompt дай описательный промпт на АНГЛИЙСКОМ языке для генерации вертикальной обложки клипа (no text, photorealistic 3d render, aspect ratio 9:16).

Выходной формат — СТРОГО JSON:
{
  "title": "Цепляющее название VK Клипа",
  "hook_first_5_sec": "Закадровый текст первых 5 секунд",
  "voiceover_script": "Полный текст дикторской озвучки на 20-30 секунд",
  "visual_cues": ["Кадр 1: Текст на экране...", "Кадр 2: Демонстрация результата..."],
  "call_to_action": "Забирай готовый промпт в Telegram по ссылке в описании!",
  "vertical_image_prompt": "Detailed English prompt for 9:16 vertical render, no text, photorealistic 3d render",
  "tags": ["vkклипы", "нейросети", "shorts", "промпты"]
}
"""

def generate_vk_clip_script(topic_or_news: str) -> dict:
    """Генерация вирального сценария VK Клипа с закадровым текстом и раскадровкой."""
    if not config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY не задан!")
        
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    prompt = f"Создай виральный сценарий VK Клипа на тему: {topic_or_news}"
    
    print(f"🎬 ИИ-Продюсер создает сценарий VK Клипа для темы: '{topic_or_news}'...")
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION_CLIPS,
            response_mime_type="application/json",
            response_schema=VKClipScript,
            temperature=0.8,
        )
    )
    
    clip_json = json.loads(response.text)
    print(f"✅ Сценарий VK Клипа '{clip_json['title']}' успешно сгенерирован!")
    return clip_json

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    test_res = generate_vk_clip_script("Как создавать готовые 3D-аватары с помощью нейросетей за 1 минуту")
    print(json.dumps(test_res, indent=2, ensure_ascii=False))
