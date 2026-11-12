import requests
import random
import time
import sys
import base64
from pathlib import Path
import config

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def try_google_nano_banana(prompt: str, output_path: Path) -> bool:
    """
    Генерация через официальный API Google Gemini Nano Banana 2.1 (Interactions API).
    Требует проект с Pay-as-you-go биллингом в Google AI Studio.
    """
    if not config.GEMINI_API_KEY:
        print("Ошибка: GEMINI_API_KEY не задан в конфигурации!")
        return False
    try:
        print("Запуск официального генератора Google Gemini Nano Banana 2.1...")
        res = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/interactions",
            headers={
                "x-goog-api-key": config.GEMINI_API_KEY,
                "Content-Type": "application/json",
                "Api-Revision": "2026-05-20"
            },
            json={
                "model": "gemini-nano-banana-2.1",
                "input": prompt,
                "response_format": {
                    "type": "image",
                    "mime_type": "image/jpeg",
                    "aspect_ratio": "16:9"
                }
            },
            timeout=50
        )
        if res.status_code == 200:
            data = res.json()
            output_image = data.get("output_image") or {}
            b64_data = output_image.get("data")
            if not b64_data and "steps" in data:
                for step in data["steps"]:
                    for item in step.get("content", []):
                        if item.get("type") == "image" and item.get("data"):
                            b64_data = item.get("data")
                            break
            if b64_data:
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(b64_data))
                print(f"✅ Обложка успешно сгенерирована через Google Nano Banana ({output_path.stat().st_size} байт): {output_path}")
                return True
        else:
            print(f"⚠️ Google Nano Banana вернул код {res.status_code}: {res.text[:160]}")
    except Exception as e:
        print(f"⚠️ Ошибка запроса к Google Nano Banana: {e}")
    return False

def generate_image(prompt: str, topic_keyword: str = "technology") -> tuple:
    """
    Генератор обложек Nano Banana для VK.
    Сервис Pollinations полностью исключен по требованию пользователя.
    """
    print(f"Генерация обложки Nano Banana: '{prompt[:60]}...'")
    
    enhanced_prompt = (
        f"{prompt}. Shot on 35mm film, Leica M11, 50mm f/1.4 lens, natural daylight, "
        f"razor sharp focus, highly detailed texture, crisp edges, authentic editorial documentary photography. "
        f"Avoid: blur, motion blur, compression artifacts, noise, distorted shapes, 3d render, cgi, cartoon, neon glow, blue holograms, glowing circuits, "
        f"robot faces, cyberpunk, plastic skin, anime, text, typography, watermark"
    )
    
    seed = random.randint(1, 1000000)
    output_path = config.IMAGE_DIR / f"vk_post_{seed}.jpg"
    
    # 1. Приоритетный нативный движок: Google Gemini Nano Banana
    if try_google_nano_banana(enhanced_prompt, output_path):
        return output_path, "google-nano-banana"

    # 2. Резерв: премиальные фото из открытого банка без водяных знаков
    print("⚠️ Прямой API Nano Banana недоступен (требуется платный API ключ с биллингом).")
    print("Загружаем чистую HD-фотографию без водяных знаков...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    fallback_urls = [
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1280&h=720&q=85",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1280&h=720&q=85",
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1280&h=720&q=85"
    ]
    
    for fb_url in fallback_urls:
        try:
            res = requests.get(fb_url, headers=headers, timeout=20)
            if res.status_code == 200 and len(res.content) > 10000:
                with open(output_path, "wb") as f:
                    f.write(res.content)
                print(f"✅ Загружена чистая HD-обложка ({len(res.content)} байт): {output_path}")
                return output_path, fb_url
        except Exception as fb_err:
            print(f"Ошибка загрузки резервной обложки: {fb_err}")
            
    print("⚠️ Не удалось получить обложку.")
    return None, None
