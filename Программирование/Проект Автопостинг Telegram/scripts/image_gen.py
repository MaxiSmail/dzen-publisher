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
    Многоядерный каскадный генератор обложек для Telegram (100% бесплатный).
    """
    print(f"Каскадная генерация обложки по промпту: '{prompt[:60]}...'")
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    output_path = config.IMAGE_DIR / f"tg_post_{seed}.jpg"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    ai_engines = [
        ("Pollinations Turbo", f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=turbo&nologo=true&seed={seed}"),
        ("Pollinations Flux-Realism", f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=flux-realism&nologo=true&seed={seed}"),
        ("Pollinations Any-Dark", f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=any-dark&nologo=true&seed={seed}"),
        ("Pollinations Flux-Anime", f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=flux-anime&nologo=true&seed={seed}")
    ]
    
    random.shuffle(ai_engines)
    
    for engine_name, url in ai_engines:
        try:
            print(f"Попытка через ИИ-движок: {engine_name}...")
            response = requests.get(url, headers=headers, timeout=25)
            if response.status_code == 200 and len(response.content) > 3000:
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
        f"https://loremflickr.com/1280/720/{urllib.parse.quote(topic_keyword)}",
        "https://loremflickr.com/1280/720/technology,ai"
    ]
    
    for fb_url in fallback_urls:
        try:
            res = requests.get(fb_url, headers=headers, allow_redirects=True, timeout=15)
            if res.status_code == 200 and len(res.content) > 3000:
                with open(output_path, "wb") as f:
                    f.write(res.content)
                print(f"✅ Резервная обложка загружена из фотобанка ({len(res.content)} байт): {output_path}")
                return output_path, fb_url
        except Exception as fb_err:
            print(f"Ошибка резервного фотобанка: {fb_err}")
            
    print("⚠️ Все попытки исчерпаны. Возврат основного URL.")
    fallback_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=turbo&nologo=true"
    return None, fallback_url
