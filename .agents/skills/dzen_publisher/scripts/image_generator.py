import urllib.parse
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
    """Генерация через Google Gemini Nano Banana 2.1 (Interactions API)."""
    if not config.GEMINI_API_KEY:
        return False
    try:
        print("Попытка генерации через Google Gemini Nano Banana 2.1...")
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
            timeout=40
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
                print(f"✅ Премиальная обложка успешно создана через Google Nano Banana 2.1 ({output_path.stat().st_size} байт): {output_path}")
                return True
        else:
            print(f"Google Nano Banana API вернул статус {res.status_code}: {res.text[:120]}")
    except Exception as e:
        print(f"Google Nano Banana API недоступен: {e}")
    return False

def generate_and_download_image(prompt: str, filename_prefix: str = "cover") -> Path:
    """
    Генератор четких журнальных обложек Nano Banana для Дзена (без мыла и артефактов).
    Исключает дешевый пластиковый ИИ-стиль (неон, роботы, 3D-рендеры).
    """
    print(f"Генерация обложки Nano Banana: '{prompt[:70]}...'")
    
    enhanced_prompt = (
        f"{prompt}. Shot on 35mm film, Leica M11, 50mm f/1.4 lens, natural soft daylight, "
        f"razor sharp focus, highly detailed textures, crisp edges, documentary aesthetic, rich colors. "
        f"Avoid: blur, motion blur, compression artifacts, noise, distorted shapes, 3d render, cgi, cartoon, neon glow, blue holograms, glowing circuits, "
        f"robot faces, cyberpunk, plastic skin, distorted hands, text, typography, watermark"
    )
    
    seed = random.randint(1, 1000000)
    output_path = config.IMAGE_DIR / f"{filename_prefix}_{seed}.jpg"
    
    # 1. Приоритет: Google Gemini Nano Banana 2.1
    if try_google_nano_banana(enhanced_prompt, output_path):
        return output_path
        
    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    # 2. Быстрые HD ИИ-движки Nano Banana и FLUX
    engines = [
        ("Pollinations Nano Banana", f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=nano-banana&nologo=true&seed={seed}"),
        ("Pollinations FLUX-Realism", f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=flux-realism&nologo=true&seed={seed}"),
        ("Pollinations FLUX", f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=flux&nologo=true&seed={seed}")
    ]
    
    for engine_name, url in engines:
        for attempt in range(2):
            try:
                print(f"Попытка генерации через {engine_name}...")
                response = requests.get(url, headers=headers, timeout=40)
                if response.status_code == 200 and len(response.content) > 10000:
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    print(f"✅ Обложка успешно сгенерирована движком '{engine_name}' ({len(response.content)} байт): {output_path}")
                    return output_path
                elif response.status_code == 402:
                    print(f"Движок '{engine_name}' вернул 402 (лимит частоты). Ожидание 3 сек...")
                    time.sleep(3)
                else:
                    print(f"⚠️ {engine_name} вернул статус: {response.status_code}")
                    break
            except Exception as e:
                print(f"⚠️ Ошибка {engine_name}: {e}")
                break
        time.sleep(1)
        
    # Резервный фотобанк
    print("⚠️ Генераторы перегружены. Загрузка из фотобанка...")
    fallback_urls = [
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1280&h=720&q=85",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1280&h=720&q=85"
    ]
    for fb in fallback_urls:
        try:
            res = requests.get(fb, headers=headers, timeout=20)
            if res.status_code == 200 and len(res.content) > 10000:
                with open(output_path, "wb") as f:
                    f.write(res.content)
                return output_path
        except Exception:
            pass
        
    raise RuntimeError("Не удалось сгенерировать качественную обложку")

if __name__ == "__main__":
    test_prompt = "Close-up of modern minimalist designer desk with laptop, notebook and cup of coffee in morning sun"
    try:
        p = generate_and_download_image(test_prompt, "test")
        print("Тест пройден:", p.exists())
    except Exception as e:
        print("Ошибка:", e)
