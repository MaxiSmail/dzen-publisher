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
    1. Напиши емкий, цепляющий пост на русском языке с использованием HTML-разметки (<b>жирный</b>, <i>курсив</i>, <code>код</code>).
    2. ДЛИНА ТЕКСТА: СТРОГО от 600 до 800 символов (включая разметку и пробелы), чтобы текст ГАРАНТИРОВАННО целиком помещался в единую подпись к фотографии в Telegram (лимит 1024 символа). Запрещено превышать 850 символов!
    3. СТРОГО БЕЗ ВОПРОСОВ В КОНЦЕ: КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО писать в конце поста вопросы для читателей, призывы к комментариям или обсуждениям. Завершай пост четким прикладным выводом или инсайтом, а не вопросом!
    4. Добавь 3-4 хэштега в конце (#промпты #нейросети #ai2026).
    5. Создай подробный английский промпт (image_prompt) для премиальной редакционной фотографии Nano Banana (Editorial Documentary Photography, 35mm film, Leica M11, мягкий дневной свет, реальные материалы).
       СТРОГО ЗАПРЕЩЕНО: Никакого 3D-рендера, CGI, киберпанка, неонового свечения, светящихся роботов и голограмм! Фото должно выглядеть как настоящий живой кадр.
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
        post_data = json.loads(response.text)
        
        # Защита от устаревшего контекста: принудительно заменяем прошлые годы на 2026
        for key in ["title", "formatted_text"]:
            if key in post_data and isinstance(post_data[key], str):
                post_data[key] = post_data[key].replace("2024", "2026").replace("2025", "2026")
        
        # Гарантируем наличие ссылки на источник
        if link and link not in post_data.get("formatted_text", ""):
            post_data["formatted_text"] += f'\n\n🔗 <a href="{link}">Читать первоисточник</a>'
            
        print("Пост успешно сгенерирован ИИ!")
        return post_data
    except Exception as e:
        print(f"Ошибка парсинга ответа от Gemini: {e}")
        raise e

if __name__ == "__main__":
    test_article = {
        "title": "OpenAI представила новую модель с поддержкой автономных агентов",
        "content": "Сегодня компания OpenAI анонсировала масштабное обновление...",
        "link": "https://example.com/test-ai-news"
    }
    try:
        res = generate_post_from_article(test_article)
        print("Сгенерированный пост:\n", res["formatted_text"])
    except Exception as e:
        print("Ошибка генерации:", e)
