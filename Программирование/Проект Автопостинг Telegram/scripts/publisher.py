import requests
import os
from pathlib import Path
import config

TELEGRAM_PROXY_URL = os.getenv("TELEGRAM_PROXY_URL")

def publish_to_telegram(formatted_text: str, image_path: Path, image_url: str = None) -> bool:
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("Ошибка: TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не найдены в .env!")
        return False
        
    print(f"Публикация поста в Telegram-канал ({config.TELEGRAM_CHAT_ID})...")
    
    proxies = None
    if TELEGRAM_PROXY_URL:
        proxies = {
            "http": TELEGRAM_PROXY_URL,
            "https": TELEGRAM_PROXY_URL
        }
        print(f"Используется прокси для Telegram: {TELEGRAM_PROXY_URL}")
    
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Попытка отправки {attempt}/{max_attempts}...")
            if image_url:
                # Отправляем как sendMessage с большой превью-картинкой сверху (лимит 4096 символов)
                url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
                payload = {
                    "chat_id": config.TELEGRAM_CHAT_ID,
                    "text": formatted_text,
                    "parse_mode": "HTML",
                    "link_preview_options": {
                        "is_disabled": False,
                        "url": image_url,
                        "prefer_large_media": True,
                        "show_above_text": True
                    }
                }
                res = requests.post(url, json=payload, timeout=30, proxies=proxies)
            else:
                # Резервный метод sendPhoto (лимит 1024 символа)
                url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendPhoto"
                with open(image_path, "rb") as photo_file:
                    payload = {
                        "chat_id": config.TELEGRAM_CHAT_ID,
                        "caption": formatted_text[:1020],
                        "parse_mode": "HTML"
                    }
                    files = {"photo": photo_file}
                    res = requests.post(url, data=payload, files=files, timeout=30, proxies=proxies)
                
            if res.status_code == 200:
                print("Пост успешно опубликован в Telegram!")
                send_admin_notification(formatted_text, success=True)
                return True
            else:
                print(f"Ошибка публикации: {res.status_code} - {res.text}")
        except Exception as e:
            print(f"Попытка {attempt} завершилась ошибкой: {e}")
            if attempt < max_attempts:
                import time
                time.sleep(5)
                
    send_admin_notification(formatted_text, success=False)
    return False

def send_admin_notification(post_text: str, success: bool = True):
    """Отправляет уведомление администратору в ЛС об успешном или неудачном выходе поста."""
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_ADMIN_CHAT_ID:
        return
        
    status_icon = "✅" if success else "❌"
    status_text = "Успешно опубликован в канал" if success else "Ошибка публикации в канал"
    
    admin_msg = (
        f"<b>{status_icon} Отчет автопостинга: {status_text}</b>\n\n"
        f"<b>Текст публикации:</b>\n"
        f"{post_text[:500]}..."
    )
    
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    proxies = {"http": TELEGRAM_PROXY_URL, "https": TELEGRAM_PROXY_URL} if TELEGRAM_PROXY_URL else None
    
    try:
        requests.post(url, json={"chat_id": config.TELEGRAM_ADMIN_CHAT_ID, "text": admin_msg, "parse_mode": "HTML"}, timeout=15, proxies=proxies)
        print("Уведомление администратору отправлено!")
    except Exception as e:
        print(f"Ошибка отправки уведомления админу: {e}")


if __name__ == "__main__":
    test_text = "🤖 <b>Тестовый пост автопостинга</b>\n\nВсё работает отлично!"
    # тест отсылки без картинки если нужно
