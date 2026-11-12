import urllib.parse
import requests
import random
import time
import sys
from pathlib import Path
import config

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def generate_image(prompt: str, topic_keyword: str = "technology") -> tuple:
    """
    Генератор фотореалистичных обложек для Telegram в редакционном стиле (FLUX).
    Исключает дешевый пластиковый ИИ-стиль (неон, роботы, 3D-рендеры).
    """
    print(f"Каскадная генерация редакционной обложки (FLUX): '{prompt[:60]}...'")
    
    # Модификаторы естественной фотографии и анти-ИИ фильтры
    enhanced_prompt = (
        f"{prompt}. Shot on 35mm film, Leica M11, 50mm f/1.4 lens, natural daylight, "
        f"subtle grain, authentic atmosphere, editorial photography. "
        f"Avoid: 3d render, cgi, cartoon, neon glow, blue holograms, glowing circuits, "
        f"robot faces, cyberpunk, plastic skin, anime, text, typography, watermark"
    )
    
    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    seed = random.randint(1, 1000000)
    output_path = config.IMAGE_DIR / f"tg_post_{seed}.jpg"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    # Только фотореалистичные модели FLUX (без аниме и турбо-мыла)
    ai_engines = [
        ("Pollinations FLUX", f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=675&model=flux&nologo=true&seed={seed}"),
        ("Pollinations FLUX-Realism", f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=675&model=flux-realism&nologo=true&seed={seed}")
    ]
    
    for engine_name, url in ai_engines:
        try:
            print(f"Попытка через ИИ-движок: {engine_name}...")
            response = requests.get(url, headers=headers, timeout=40)
            if response.status_code == 200 and len(response.content) > 10000:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Обложка успешно сгенерирована движком '{engine_name}' ({len(response.content)} байт): {output_path}")
                return output_path, url
            else:
                print(f"Движок '{engine_name}' вернул код: {response.status_code}")
        except Exception as e:
            print(f"Движок '{engine_name}' недоступен: {e}")
        time.sleep(1)

    print("⚠️ ИИ-движки перегружены. Загружаем HD-фотографию из резервного фотобанка...")
    fallback_urls = [
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&h=675&q=80",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&h=675&q=80"
    ]
    
    for fb_url in fallback_urls:
        try:
            res = requests.get(fb_url, headers=headers, timeout=20)
            if res.status_code == 200 and len(res.content) > 10000:
                with open(output_path, "wb") as f:
                    f.write(res.content)
                print(f"✅ Резервная обложка загружена ({len(res.content)} байт): {output_path}")
                return output_path, fb_url
        except Exception as fb_err:
            print(f"Ошибка резервного фотобанка: {fb_err}")
            
    print("⚠️ Все попытки исчерпаны.")
    return None, None
