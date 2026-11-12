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
    
    has_image = image_path and Path(image_path).exists() and Path(image_path).stat().st_size > 1000
    
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Попытка отправки {attempt}/{max_attempts}...")
            
            if has_image:
                # 1. Приоритетный метод: Прямая загрузка реального фото через sendPhoto
                url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendPhoto"
                
                if len(formatted_text) <= 1024:
                    with open(image_path, "rb") as photo_file:
                        payload = {
                            "chat_id": config.TELEGRAM_CHAT_ID,
                            "caption": formatted_text,
                            "parse_mode": "HTML"
                        }
                        files = {"photo": photo_file}
                        res = requests.post(url, data=payload, files=files, timeout=35, proxies=proxies)
                else:
                    # Если текст длиннее 1024 символов (лимит caption)
                    # Отправляем фото с первым блоком, затем второе сообщение с полным текстом
                    with open(image_path, "rb") as photo_file:
                        payload = {
                            "chat_id": config.TELEGRAM_CHAT_ID,
                            "caption": formatted_text[:1020],
                            "parse_mode": "HTML"
                        }
                        files = {"photo": photo_file}
                        res = requests.post(url, data=payload, files=files, timeout=35, proxies=proxies)
                    
                    # Отправляем остаток текста сообщением
                    remainder = formatted_text[1020:].strip()
                    if remainder:
                        msg_url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
                        requests.post(msg_url, json={
                            "chat_id": config.TELEGRAM_CHAT_ID,
                            "text": remainder,
                            "parse_mode": "HTML"
                        }, timeout=20, proxies=proxies)
            else:
                # 2. Если фото не сгенерировалось - отправка чистого текста
                url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
                payload = {
                    "chat_id": config.TELEGRAM_CHAT_ID,
                    "text": formatted_text,
                    "parse_mode": "HTML"
                }
                res = requests.post(url, json=payload, timeout=30, proxies=proxies)
                
            if res.status_code == 200:
                print("✅ Пост с обложкой успешно опубликован в Telegram!")
                send_admin_notification(formatted_text, success=True)
                return True
            else:
                print(f"Ошибка публикации в Telegram: {res.status_code} - {res.text}")
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
