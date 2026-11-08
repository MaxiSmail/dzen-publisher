import os
import sys
import logging
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.exceptions import TelegramNetworkError

# UTF-8 консоль Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_ID = os.getenv("ALLOWED_USER_ID")
PROXY_URL = os.getenv("PROXY_URL") # Например: http://127.0.0.1:10808 или socks5://127.0.0.1:1080
CUSTOM_API_SERVER = os.getenv("TELEGRAM_API_SERVER") # Например: https://tg-proxy.ru

DEFAULT_VAULT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Obsidian"))
VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", DEFAULT_VAULT_PATH)
DAILY_PATH = os.path.join(VAULT_PATH, "Daily")

logging.basicConfig(level=logging.INFO)

if not BOT_TOKEN:
    print("[ERROR] TELEGRAM_BOT_TOKEN не найден в .env")
    sys.exit(1)

def append_to_daily(text_note: str) -> str:
    os.makedirs(DAILY_PATH, exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M")
    daily_file = os.path.join(DAILY_PATH, f"{today_str}.md")
    
    note_entry = f"\n- 📱 **[{time_str}] (Из Telegram):** {text_note.strip()}"
    
    if not os.path.exists(daily_file):
        initial_header = f"---\ntitle: \"Журнал {today_str}\"\ntype: conversation\ncreated: {today_str}\n---\n\n# 📅 Ежедневный Журнал {today_str}\n\n## 📝 Быстрые заметки\n"
        with open(daily_file, "w", encoding="utf-8") as f:
            f.write(initial_header)
            
    with open(daily_file, "a", encoding="utf-8") as f:
        f.write(note_entry)
        
    return daily_file

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Привет, Максим! Я ваш Telegram-мост для Obsidian.\n\nПросто отправьте мне любой текст или идею, и я мгновенно сохраню её в ваш журнал Obsidian!")

@dp.message(F.text)
async def handle_text_note(message: types.Message):
    if ALLOWED_USER_ID and str(message.from_user.id) != str(ALLOWED_USER_ID):
        await message.answer("⚠️ Доступ ограничен.")
        return

    note_text = message.text
    saved_file = append_to_daily(note_text)
    file_name = os.path.basename(saved_file)
    
    await message.answer(f"✅ **Заметка сохранена!**\n📄 Добавлено в: `{file_name}`.")

async def start_bot():
    kwargs = {"timeout": 60}
    if PROXY_URL:
        kwargs["proxy"] = PROXY_URL
        print(f"[INFO] Используется прокси: {PROXY_URL}")
        
    if CUSTOM_API_SERVER:
        kwargs["api"] = TelegramAPIServer.from_base(CUSTOM_API_SERVER)
        print(f"[INFO] Используется кастомный сервер API: {CUSTOM_API_SERVER}")
        
    session = AiohttpSession(**kwargs)
    bot = Bot(token=BOT_TOKEN, session=session)
    
    print("[INFO] Telegram-бот запущен и ожидает сообщений...")
    while True:
        try:
            await dp.start_polling(bot, handle_signals=False)
        except (TelegramNetworkError, Exception) as e:
            print(f"[WARNING] Сетевой сбой подключения к Telegram ({e}). Повтор через 5 секунд...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(start_bot())
