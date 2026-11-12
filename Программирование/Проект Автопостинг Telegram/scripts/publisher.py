import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
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
    url_photo = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendPhoto"
    url_msg = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Попытка отправки {attempt}/{max_attempts}...")
            
            if has_image:
                # 1. Попытка единого сообщения (если текст укладывается в лимит 1024 символа)
                if len(formatted_text) <= 1024:
                    with open(image_path, "rb") as photo_file:
                        res = requests.post(url_photo, data={
                            "chat_id": config.TELEGRAM_CHAT_ID,
                            "caption": formatted_text,
                            "parse_mode": "HTML"
                        }, files={"photo": photo_file}, timeout=35, proxies=proxies)
                        
                    if res.status_code == 200:
                        print("✅ Пост с обложкой успешно опубликован в Telegram (единое фото-сообщение)!")
                        send_admin_notification(formatted_text, success=True)
                        return True
                    else:
                        print(f"⚠️ Одиночная отправка фото не прошла ({res.status_code}: {res.text}). Переход на гарантированный раздельный режим...")

                # 2. Гарантированный надежный режим: Фото + полный текст без риска сломать HTML-теги
                with open(image_path, "rb") as photo_file:
                    res_p = requests.post(url_photo, data={
                        "chat_id": config.TELEGRAM_CHAT_ID
                    }, files={"photo": photo_file}, timeout=35, proxies=proxies)
                
                # Отправляем полный текст сообщения
                res_m = requests.post(url_msg, json={
                    "chat_id": config.TELEGRAM_CHAT_ID,
                    "text": formatted_text,
                    "parse_mode": "HTML"
                }, timeout=30, proxies=proxies)
                
                if res_m.status_code != 200:
                    # Если разметка HTML содержит ошибку от Gemini - очищаем и отправляем чистый текст
                    print(f"⚠️ Ошибка HTML ({res_m.text}). Отправляем чистый текст...")
                    clean_text = BeautifulSoup(formatted_text, "html.parser").get_text()
                    res_m = requests.post(url_msg, json={
                        "chat_id": config.TELEGRAM_CHAT_ID,
                        "text": clean_text
                    }, timeout=30, proxies=proxies)
                    
                if res_m.status_code == 200:
                    print("✅ Пост с обложкой успешно опубликован в Telegram (фото + текст)!")
                    send_admin_notification(formatted_text, success=True)
                    return True
                else:
                    print(f"Ошибка отправки текста: {res_m.status_code} - {res_m.text}")
                    
            else:
                # 3. Резервный режим без картинки
                res_m = requests.post(url_msg, json={
                    "chat_id": config.TELEGRAM_CHAT_ID,
                    "text": formatted_text,
                    "parse_mode": "HTML"
                }, timeout=30, proxies=proxies)
                
                if res_m.status_code == 200:
                    print("Пост без обложки успешно опубликован в Telegram!")
                    send_admin_notification(formatted_text, success=True)
                    return True
                else:
                    print(f"Ошибка отправки текста: {res_m.status_code} - {res_m.text}")

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
