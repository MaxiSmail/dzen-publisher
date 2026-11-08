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
from typing import List, Optional
import config

class VKPost(BaseModel):
    title: str
    formatted_text: str
    image_prompt: str
    tags: List[str]
    poll_question: Optional[str] = None
    poll_options: Optional[List[str]] = None


def get_gemini_client():
    if not config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY не задан в .env!")
    return genai.Client(api_key=config.GEMINI_API_KEY)

def generate_post_from_rss(article_data: dict) -> dict:
    """Генерация уникального утреннего поста для ВК на основе RSS-новости."""
    client = get_gemini_client()
    
    raw_title = article_data.get("title", "")
    raw_content = article_data.get("content", "")
    
    prompt = f"""
    На основе следующей новости создай глубокий практический пост для ВК.
    
    НОВОСТЬ: {raw_title}
    ОПИСАНИЕ:
    {raw_content}
    
    Требования:
    1. Перепиши новость, объяснив её практическую важность.
    2. Обязательно добавь практическую ценность: готовый промпт (выделив его строками с >>>) и пошаговую мини-инструкцию по применению описанной технологии.
    3. Пост не должен содержать HTML тегов!
    """
    
    print(f"Запрос к Gemini API для генерации VK-поста из RSS: '{raw_title}'...")
    return _generate_with_gemini(client, prompt)

def adapt_dzen_article_to_vk(dzen_title: str, dzen_content: str) -> dict:
    """Адаптация длинной статьи из Дзена под формат ВКонтакте (очистка от HTML, форматирование промптов)."""
    client = get_gemini_client()
    
    prompt = f"""
    Адаптируй следующую статью из нашего Дзен-канала под публикацию на стене ВКонтакте.
    
    ЗАГОЛОВОК ДЗЕНА: {dzen_title}
    СОДЕРЖИМОЕ СТАТЬИ:
    {dzen_content}
    
    Требования к адаптации:
    1. Очисти текст от всех HTML-тегов.
    2. Отформатируй все блоки кода и шаблоны промптов текстовыми символами >>> с отступами.
    3. Сохрани глубокую экспертность, мастер-класс и лид-магниты (CTA).
    4. Создай новый уникальный сюжетный image_prompt на английском языке для генерации обложки.
    """
    
    print(f"Запрос к Gemini API для адаптации Дзен-статьи: '{dzen_title}'...")
    return _generate_with_gemini(client, prompt)

def _generate_with_gemini(client, prompt: str) -> dict:
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=config.SYSTEM_INSTRUCTION_VK,
                    response_mime_type="application/json",
                    response_schema=VKPost,
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
        print("Пост успешно сгенерирован ИИ для ВКонтакте!")
        return post_json
    except Exception as e:
        print(f"Ошибка парсинга ответа от Gemini: {e}")
        print("Сырой ответ:", response.text)
        raise e

if __name__ == "__main__":
    # Тестовый запуск
    import dotenv
    dotenv.load_dotenv()
    test_article = {
        "title": "Вышел новый ИИ-генератор музыки Suno v4",
        "link": "https://example.com/suno4",
        "content": "Компания Suno сегодня объявила о выпуске четвертого поколения своего музыкального искусственного интеллекта..."
    }
    try:
        res = generate_post_from_rss(test_article)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        
        print("\n--- ТЕСТ АДАПТАЦИИ СТАТЬИ ДЗЕНА ---")
        res_dzen = adapt_dzen_article_to_vk("5 способов ускорить Python в 2026 году", "Python остается самым популярным языком для ИИ, но он медленный. В этой статье мы рассмотрим 5 практических трюков: от компилятора Numba до использования библиотек на Rust. Шаблон промпта для рефакторинга кода в GPT-4o: [вставить промпт].")
        print(json.dumps(res_dzen, indent=2, ensure_ascii=False))
    except Exception as e:
        print("Ошибка при тестировании:", e)
