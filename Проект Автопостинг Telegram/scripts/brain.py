import json
import time
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel
from typing import List
import config

class TelegramPost(BaseModel):
    title: str
    formatted_text: str
    image_prompt: str
    tags: List[str]

def get_gemini_client():
    if not config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY не задан в .env!")
    return genai.Client(api_key=config.GEMINI_API_KEY)

def generate_post_from_article(article_data: dict) -> dict:
    client = get_gemini_client()
    
    raw_title = article_data.get("title", "")
    raw_content = article_data.get("content", "")
    link = article_data.get("link", "")
    
    prompt = f"""
    Адаптируй следующую новость в виральный пост для Telegram-канала:
    
    ОРИГИНАЛЬНЫЙ ЗАГОЛОВОК: {raw_title}
    ТЕКСТ НОВОСТИ:
    {raw_content}
    
    Требования:
    1. Напиши цепляющий пост на русском языке с использованием HTML-разметки (<b>жирный</b>, <i>курсив</i>).
    2. Добавь 3-5 хэштегов в конце.
    3. Создай подробный английский промпт (image_prompt) для футуристичной 3D-иллюстрации к новости. Не вставляй ссылки на сторонние сайты.
    """
    
    print(f"Запрос к Gemini API для переработки статьи: '{raw_title}'...")
    
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=config.SYSTEM_INSTRUCTION,
                    response_mime_type="application/json",
                    response_schema=TelegramPost,
                    temperature=0.7,
                )
            )
            break
        except APIError as e:
            if attempt < max_attempts - 1:
                print(f"Ошибка API ({e.code}). Повтор через 10 секунд...")
                time.sleep(10)
            else:
                raise e

    try:
        post_json = json.loads(response.text)
        
        text = post_json.get("formatted_text", "")
        cta = config.MONETIZATION_CTA if config.MONETIZATION_CTA else ""
        
        # Гарантированная защита от превышения лимита Telegram (4096 символов для sendMessage)
        max_text_len = 4000 - len(cta)
        if len(text) > max_text_len:
            text = text[:max_text_len - 3] + "..."
            
        if cta and cta.strip() not in text:
            text += cta
            
        post_json["formatted_text"] = text
        print(f"Пост успешно сгенерирован ИИ! Длина подписи: {len(text)} символов.")
        return post_json
    except Exception as e:
        print(f"Ошибка парсинга ответа от Gemini: {e}")
        print("Сырой ответ:", response.text)
        raise e

if __name__ == "__main__":
    test_article = {
        "title": "OpenAI представила новую модель GPT-5",
        "link": "https://example.com/gpt5",
        "content": "Компания OpenAI сегодня официально объявила о выходе новой флагманской нейросети..."
    }
    res = generate_post_from_article(test_article)
    print(json.dumps(res, indent=2, ensure_ascii=False))
