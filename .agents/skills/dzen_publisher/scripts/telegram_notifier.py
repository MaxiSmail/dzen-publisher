import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_notification(title: str, tags: list, screenshot_path: Path = None, extra_info: str = "") -> bool:
    """
    Отправляет уведомление в Telegram с заголовком статьи, тегами и скриншотом публикации.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram-уведомления отключены (TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не указаны в .env/Secrets).")
        return False

    print("=" * 60)
    print("ОТПРАВКА УВЕДОМЛЕНИЯ В TELEGRAM")
    print("=" * 60)

    tags_str = " ".join([f"#{t.replace(' ', '_')}" for t in tags]) if tags else ""
    
    caption = (
        f"🚀 <b>[ИИ-Директор Дзена] Новый материал опубликован!</b>\n\n"
        f"📌 <b>Заголовок:</b> {title}\n"
        f"🏷 <b>Теги:</b> {tags_str}\n"
        f"{extra_info}\n"
        f"🤖 <i>Статья сгенерирована и опубликована полностью автономно.</i>"
    )

    try:
        # Если есть скриншот публикации, отправляем с фото
        if screenshot_path and Path(screenshot_path).exists():
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            with open(screenshot_path, "rb") as photo_file:
                payload = {
                    "chat_id": TELEGRAM_CHAT_ID,
                    "caption": caption,
                    "parse_mode": "HTML"
                }
                files = {"photo": photo_file}
                res = requests.post(url, data=payload, files=files, timeout=20)
        else:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": caption,
                "parse_mode": "HTML"
            }
            res = requests.post(url, json=payload, timeout=20)

        if res.status_code == 200:
            print("Уведомление в Telegram успешно доставлено!")
            return True
        else:
            print(f"Ошибка отправки Telegram-уведомления: {res.status_code} - {res.text}")
            return False

    except Exception as e:
        print(f"Не удалось отправить уведомление в Telegram: {e}")
        return False

if __name__ == "__main__":
    # Тест отсылки
    send_telegram_notification("Тестовый заголовок ИИ", ["ии", "нейросети"])
