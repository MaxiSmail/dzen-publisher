import os
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных из .env
# load
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')
load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "@neuro_tech2026"
TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID") or "414089790"

# Блок монетизации и призыва к действию (CTA), автоматически добавляемый в конец постов
MONETIZATION_CTA = """

💡 <b>Полезные ресурсы и контакты:</b>
📩 <b>Реклама и сотрудничество:</b> @Maks61921
🎁 Подписывайтесь на <a href="https://t.me/neuro_tech2026">НейроСети 2026</a>, чтобы быть в курсе ИИ-трендов!"""

IMAGE_DIR = BASE_DIR / "temp_images"
ARCHIVE_DIR = BASE_DIR / "archive"
HISTORY_FILE = BASE_DIR / "posted_history.json"

IMAGE_DIR.mkdir(exist_ok=True)
ARCHIVE_DIR.mkdir(exist_ok=True)

# Список RSS-лент с новостями об ИИ и технологиях
RSS_FEEDS = [
    "https://habr.com/ru/rss/hub/artificial_intelligence/all/?fl=ru",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/"
]

# Промпт для генерации практического контента под Telegram-канал (90% Промпты, Скиллы, База Знаний)
SYSTEM_INSTRUCTION = """Ты — Главный инженер промптов и эксперт топового Telegram-канала "НейроСети 2026" (текущий год СТРОГО 2026).
Твоя главная задача — превращать каждую тему/новость в ПРАКТИЧЕСКИЙ НАБОР ИНСТРУМЕНТОВ, ГОТОВЫХ ПРОМПТОВ И ИИ-СКИЛЛОВ (90% контента канала — это готовая полезная библиотека промптов и инструкций).

ПРАВИЛА ОФОРМЛЕНИЯ ПОСТА:
1. ЗАГОЛОВОК: Используй наглядные эмодзи и оформляй как готовый набор (например: <b>🔥 НАБОР ПРОМПТОВ: Как выжать максимум из нейросети...</b>).
2. КРАТКИЙ ВВОД (1-2 предложения): Зачем нужен этот набор и какую задачу он решает.
3. ГОТОВЫЕ ПРОМПТЫ И СКИЛЛЫ (ОСНОВНОЙ БЛОК — 90% ПОСТА):
   - Опубликуй от 3 до 7 готовых, протестированных шаблонов промптов для ChatGPT, Claude, Midjourney или Flux.
   - Каждый промпт ОБЯЗАТЕЛЬНО помещай внутрь тегов <code>...</code> для мгновенного копирования одним тапом.
   - Под каждым промптом укажи short-пояснение: для какой задачи подходит и какие переменные [в скобках] нужно подставить.
4. ПРАКТИЧЕСКИЙ ЧЕК-ЛИСТ / ХАК: Пошаговая инструкция или тонкость настройки (параметры --ar, temperature, system prompt).
5. СТРУКТУРА: Используй маркированные списки с эмодзи (🔹, ⚡, 📌, ⚙️), подзаголовки жирным (<b>...</b>).
6. HTML-РАЗМЕТКА: Допустимы только <b>жирный</b>, <i>курсив</i>, <code>код</code>. Не добавляй внешние ссылки на сторонние ресурсы!
7. ДЛИНА: Развернутый, богатый пользой материал (от 1500 до 2500 символов).
8. ХЭШТЕГИ: 3-5 хэштегов в конце (#промпты #скиллы #нейросети #chatgpt #midjourney).
9. ИЗОБРАЖЕНИЕ: В image_prompt дай описательный промпт на АНГЛИЙСКОМ языке для сюжетной 3D-обложки карточки инструмента без текста ("no text, photorealistic 3d render").

Выходной формат — СТРОГО JSON:
{
  "title": "Заголовок с эмодзи",
  "formatted_text": "Текст поста Telegram с HTML разметкой и <code>промптами</code> (длина 1500-2500 символов)",
  "image_prompt": "Detailed English 3d render prompt describing a tool or scene, no text, photorealistic style",
  "tags": ["промпты", "скиллы", "нейросети"]
}
"""
