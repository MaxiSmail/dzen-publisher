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

def try_huggingface_flux(prompt: str, output_path: Path) -> bool:
    """
    Генерация через официальный Hugging Face Serverless API: Black Forest Labs FLUX.1 [schnell].
    Полностью бесплатно, без водяных знаков, максимальная фотореалистичность.
    """
    if not config.HF_TOKEN:
        return False
    try:
        print("Попытка генерации через Hugging Face (FLUX.1-schnell)...")
        api_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
        headers = {
            "Authorization": f"Bearer {config.HF_TOKEN}",
            "User-Agent": "Mozilla/5.0"
        }
        payload = {
            "inputs": prompt,
            "parameters": {
                "num_inference_steps": 4,
                "width": 1024,
                "height": 576
            }
        }
        
        for attempt in range(3):
            res = requests.post(api_url, headers=headers, json=payload, timeout=60)
            if res.status_code == 200 and len(res.content) > 10000:
                with open(output_path, "wb") as f:
                    f.write(res.content)
                print(f"✅ Премиальная обложка FLUX.1 успешно сгенерирована через Hugging Face ({len(res.content)} байт): {output_path}")
                return True
            elif res.status_code == 503:
                data = res.json() if "application/json" in res.headers.get("content-type", "") else {}
                est_time = data.get("estimated_time", 15)
                print(f"Hugging Face прогревает модель (ожидание ~{est_time:.0f}с)...")
                time.sleep(min(est_time, 20))
            else:
                print(f"Hugging Face API вернул код {res.status_code}: {res.text[:120]}")
                break
    except Exception as e:
        print(f"Hugging Face API недоступен: {e}")
    return False

def try_google_nano_banana(prompt: str, output_path: Path) -> bool:
    """Генерация через официальный API Google Gemini Nano Banana 2.1."""
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
                print(f"✅ Премиальная обложка успешно сгенерирована через Google Nano Banana ({output_path.stat().st_size} байт): {output_path}")
                return True
        else:
            print(f"Google Nano Banana вернул код {res.status_code}: {res.text[:120]}")
    except Exception as e:
        print(f"Google Nano Banana API недоступен: {e}")
    return False

def generate_and_download_image(prompt: str, filename_prefix: str = "cover") -> Path:
    """
    Генератор обложек FLUX / Nano Banana для Дзена БЕЗ водяных знаков.
    """
    print(f"Генерация фотореалистичной обложки для Дзена: '{prompt[:70]}...'")
    
    enhanced_prompt = (
        f"{prompt}. Shot on 35mm film, Leica M11, 50mm f/1.4 lens, natural soft daylight, "
        f"razor sharp focus, highly detailed textures, crisp edges, documentary aesthetic, rich colors. "
        f"Avoid: blur, motion blur, compression artifacts, noise, distorted shapes, 3d render, cgi, cartoon, neon glow, blue holograms, glowing circuits, "
        f"robot faces, cyberpunk, plastic skin, distorted hands, text, typography, watermark"
    )
    
    seed = random.randint(1, 1000000)
    output_path = config.IMAGE_DIR / f"{filename_prefix}_{seed}.jpg"
    
    # 1. Приоритет: Hugging Face FLUX.1 [schnell]
    if try_huggingface_flux(enhanced_prompt, output_path):
        return output_path
        
    # 2. Приоритет: Google Gemini Nano Banana 2.1
    if try_google_nano_banana(enhanced_prompt, output_path):
        return output_path
        
    # 3. Резервный фотобанк без водяных знаков
    print("⚠️ API-генераторы недоступны. Загружаем HD-фотографию из открытого фотобанка...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    fallback_urls = [
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1280&h=720&q=85",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1280&h=720&q=85",
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1280&h=720&q=85"
    ]
    for fb in fallback_urls:
        try:
            res = requests.get(fb, headers=headers, timeout=20)
            if res.status_code == 200 and len(res.content) > 10000:
                with open(output_path, "wb") as f:
                    f.write(res.content)
                print(f"✅ Загружена чистая HD-обложка ({len(res.content)} байт): {output_path}")
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
