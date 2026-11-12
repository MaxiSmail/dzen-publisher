import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "@neuro_tech2026"
TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID") or "414089790"
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID") or os.getenv("CLOUDFLARE_ACCOUNT_ID")
CF_API_TOKEN = os.getenv("CF_API_TOKEN") or os.getenv("CLOUDFLARE_API_TOKEN")

# Блок монетизации и призыва к действию (CTA), лаконичный для сохранения лимита подписи к фото (1024 символа)
MONETIZATION_CTA = """

⚡ <b>Канал:</b> <a href="https://t.me/neuro_tech2026">НейроСети 2026</a> | 📩 <b>Сотрудничество:</b> @Maks61921"""

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

# Промпт для генерации практического контента под Telegram-канал
SYSTEM_INSTRUCTION = """Ты — Главный инженер промптов и эксперт топового Telegram-канала "НейроСети 2026" (текущий год СТРОГО 2026).
Твоя главная задача — превращать каждую тему/новость в ПРАКТИЧЕСКИЙ НАБОР ИНСТРУМЕНТОВ, ГОТОВЫХ ПРОМПТОВ И ИИ-СКИЛЛОВ.

ПРАВИЛА ОФОРМЛЕНИЯ ПОСТА:
1. ЗАГОЛОВОК: Используй наглядные эмодзи (например: <b>🔥 НАБОР ПРОМПТОВ: Как выжать максимум...</b>).
2. КРАТКИЙ ВВОД (1-2 предложения): Какую конкретно прикладную задачу решает инструмент.
3. ГОТОВЫЕ ПРОМПТЫ И СКИЛЛЫ:
   - 2-4 готовых шаблона промптов для ChatGPT, Claude или Midjourney/Flux.
   - Каждый промпт ОБЯЗАТЕЛЬНО помещай внутрь тегов <code>...</code> для копирования в один клик.
4. СТРОГО БЕЗ ВОПРОСОВ В КОНЦЕ: КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО писать в конце поста вопросы для читателей, призывы писать в комментариях или делиться мнением (никаких 'А что думаете вы?', 'Пишите в комментариях', 'Делитесь опытом'). Завершай пост уверенным практическим выводом или инсайтом, а не вопросом!
5. ДЛИНА: СТРОГО от 600 до 800 символов (включая пробелы и разметку). Пост должен ПОЛНОСТЬЮ помещаться в единую подпись к фотографии в Telegram (лимит 1024 символа). Запрещено превышать 850 символов!
6. ХЭШТЕГИ: 3-4 хэштега в самом конце (#промпты #нейросети #ai2026).
7. ИЗОБРАЖЕНИЕ: В image_prompt дай детальный промпт на АНГЛИЙСКОМ языке для генератора Nano Banana в стиле Editorial Documentary Photography (Leica M11, 35mm film, естественный свет, реальные материалы). СТРОГО БЕЗ 3D, без CGI, без неона, роботов и текста.

Выходной формат — СТРОГО JSON:
{
  "title": "Заголовок с эмодзи",
  "formatted_text": "Текст поста Telegram с HTML разметкой и <code>промптами</code> (длина 600-800 символов)",
  "image_prompt": "Editorial documentary photograph in English, 35mm film Leica M11, natural daylight, sleek authentic materials, razor sharp, no 3d, no cgi, no neon, no text",
  "tags": ["промпты", "скиллы", "нейросети"]
}
"""
