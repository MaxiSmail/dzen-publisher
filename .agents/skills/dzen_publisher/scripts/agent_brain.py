import json
import random
from pathlib import Path
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List
import config

class DzenArticle(BaseModel):
    title: str
    content: str
    image_prompt: str
    tags: List[str]

def get_gemini_client():
    if not config.GEMINI_API_KEY:
        raise ValueError("Критическая ошибка: GEMINI_API_KEY не установлен в файле .env!")
    return genai.Client(api_key=config.GEMINI_API_KEY)

def generate_article(analytics_data: dict = None) -> dict:
    client = get_gemini_client()
    
    base_category = random.choice(config.TOPICS)
    
    # Формируем контекст аналитики для адаптации ИИ
    analytics_context = ""
    if analytics_data and "recommendations" in analytics_data:
        recs = "\n- ".join(analytics_data["recommendations"])
        analytics_context = f"\nАналитические рекомендации по развитию канала:\n- {recs}\n"
    
    prompt = f"""
    Ты — Директор и Главный редактор ведущего русскоязычного Дзен-канала об Искусственном Интеллекте.
    Наша главная цель — набрать 30 часов дочитываний от ПОДПИСЧИКОВ для быстрой активации МОНЕТИЗАЦИИ канала.
    
    Тема текущей публикации: "{base_category}".
    {analytics_context}
    
    Требования к статье для максимального удержания и подписок:
    1. ОГРОМНАЯ ПРАКТИЧЕСКАЯ ЦЕННОСТЬ: Дай читателю ценный урок, мастер-класс, пошаговый разбор ИИ-инструмента или готовые шаблоны промптов, которые можно применить прямо сейчас.
    2. ПРИЗЫВ К ПОДПИСКЕ (CTA): Вставьте ненавязчивый, но убедительный призыв подписаться на канал (например: "Подпишитесь на наш канал, чтобы ежедневно получать свежие гайды по нейросетям и не потерять этот материал!").
    3. СТРУКТУРА ДЛЯ УДЕРЖАНИЯ ВНИМАНИЯ:
       - Завлекающее введение с проблемой.
       - Заголовки разделов пиши ЗАГЛАВНЫМИ БУКВАМИ на отдельной строке (например, "ПОШАГОВЫЙ АЛГОРИТМ").
       - Наглядные списки с тире.
       - Открытый ВОПРОС в конце для стимуляции обсуждения в комментариях.
    4. ДЛИНА: Полноценный качественный лонгрид (от 3000 до 4500 символов) для набора минут просмотра.
    5. Промпт для изображения (image_prompt) на АНГЛИЙСКОМ языке (футуристичная 3D-иллюстрация без текста).
    6. От 5 до 8 тематических хэштегов.
    """
    
    print(f"Запуск генерации адаптивного ИИ-материала по теме: {base_category}...")
    
    from google.genai.errors import APIError
    import time
    
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=config.SYSTEM_INSTRUCTION,
                    response_mime_type="application/json",
                    response_schema=DzenArticle,
                    temperature=0.75,
                )
            )
            break
        except APIError as e:
            if e.code in [429, 503] and attempt < max_attempts - 1:
                wait_time = (attempt + 1) * 15
                print(f"Временная ошибка API ({e.code}: {e.message}). Повторная попытка через {wait_time} секунд...")
                time.sleep(wait_time)
            else:
                print(f"Не удалось обойти ошибку API на попытке {attempt + 1}: {e}")
                raise e
    
    try:
        article_data = json.loads(response.text)
        print("Адаптивная ИИ-статья успешно сгенерирована!")
        print(f"Заголовок: {article_data.get('title')}")
        print(f"Теги: {article_data.get('tags')}")
        return article_data
    except Exception as e:
        print(f"Ошибка парсинга ответа от Gemini: {e}")
        print("Сырой ответ модели:")
        print(response.text)
        raise e

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    try:
        article = generate_article()
        print(json.dumps(article, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Ошибка при тесте: {e}")
