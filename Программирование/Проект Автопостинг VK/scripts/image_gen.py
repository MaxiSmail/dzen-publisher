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

def try_cloudflare_flux(prompt: str, output_path: Path) -> bool:
    """
    Генерация через официальный Cloudflare Workers AI: Black Forest Labs FLUX.1 [schnell].
    Полностью бесплатно (10 000 нейронов/день), без водяных знаков, фотореализм высшего уровня.
    """
    if not config.CF_ACCOUNT_ID or not config.CF_API_TOKEN:
        return False
    try:
        print("Попытка генерации через Cloudflare Workers AI (FLUX.1-schnell)...")
        api_url = f"https://api.cloudflare.com/client/v4/accounts/{config.CF_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"
        headers = {
            "Authorization": f"Bearer {config.CF_API_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt,
            "steps": 4
        }
        res = requests.post(api_url, headers=headers, json=payload, timeout=60)
        if res.status_code == 200:
            content_type = res.headers.get("content-type", "")
            if "image" in content_type and len(res.content) > 10000:
                with open(output_path, "wb") as f:
                    f.write(res.content)
                print(f"✅ Обложка FLUX.1 успешно сгенерирована через Cloudflare ({len(res.content)} байт): {output_path}")
                return True
            elif "json" in content_type:
                data = res.json()
                if "result" in data and "image" in data["result"]:
                    img_bytes = base64.b64decode(data["result"]["image"])
                    with open(output_path, "wb") as f:
                        f.write(img_bytes)
                    print(f"✅ Обложка FLUX.1 успешно сгенерирована через Cloudflare ({len(img_bytes)} байт): {output_path}")
                    return True
                else:
                    print(f"Cloudflare вернул unexpected JSON: {list(data.keys())}")
        else:
            print(f"Cloudflare Workers AI вернул код {res.status_code}: {res.text[:120]}")
    except Exception as e:
        print(f"Cloudflare Workers AI API недоступен: {e}")
    return False

def try_huggingface_flux(prompt: str, output_path: Path) -> bool:
    """Генерация через Hugging Face Serverless (резерв)."""
    if not config.HF_TOKEN:
        return False
    try:
        print("Попытка генерации через Hugging Face...")
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
        res = requests.post(api_url, headers=headers, json=payload, timeout=40)
        if res.status_code == 200 and len(res.content) > 10000:
            with open(output_path, "wb") as f:
                f.write(res.content)
            print(f"✅ Обложка сгенерирована через Hugging Face ({len(res.content)} байт): {output_path}")
            return True
    except Exception as e:
        print(f"Hugging Face API недоступен: {e}")
    return False

def try_google_nano_banana(prompt: str, output_path: Path) -> bool:
    """Генерация через официальный API Google Gemini Nano Banana 2.1 (резерв)."""
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
                print(f"✅ Обложка успешно сгенерирована через Google Nano Banana ({output_path.stat().st_size} байт): {output_path}")
                return True
    except Exception as e:
        print(f"Google Nano Banana API недоступен: {e}")
    return False

def generate_image(prompt: str, topic_keyword: str = "technology") -> tuple:
    """
    Генератор премиальных фотореалистичных обложек для ВКонтакте БЕЗ водяных знаков.
    Приоритет 1: Cloudflare Workers AI FLUX.1 [schnell].
    Приоритет 2: Hugging Face FLUX.1.
    Приоритет 3: Google Gemini Nano Banana.
    Резерв: Чистая HD-фотография из открытого фотобанка.
    """
    print(f"Генерация фотореалистичной обложки для VK: '{prompt[:60]}...'")
    
    enhanced_prompt = (
        f"{prompt}. Shot on 35mm film, Leica M11, 50mm f/1.4 lens, natural daylight, "
        f"razor sharp focus, highly detailed texture, crisp edges, authentic editorial documentary photography. "
        f"Avoid: blur, motion blur, compression artifacts, noise, distorted shapes, 3d render, cgi, cartoon, neon glow, blue holograms, glowing circuits, "
        f"robot faces, cyberpunk, plastic skin, anime, text, typography, watermark"
    )
    
    seed = random.randint(1, 1000000)
    output_path = config.IMAGE_DIR / f"vk_post_{seed}.jpg"
    
    # 1. Приоритет: Cloudflare Workers AI FLUX.1 [schnell]
    if try_cloudflare_flux(enhanced_prompt, output_path):
        return output_path, "cloudflare-flux-schnell"
        
    # 2. Резерв: Hugging Face FLUX.1
    if try_huggingface_flux(enhanced_prompt, output_path):
        return output_path, "huggingface-flux-schnell"

    # 3. Резерв: Google Gemini Nano Banana 2.1
    if try_google_nano_banana(enhanced_prompt, output_path):
        return output_path, "google-nano-banana"

    # 4. Резерв: чистые фотографии высокого разрешения без водяных знаков
    print("⚠️ API-генераторы недоступны. Загружаем HD-фотографию из открытого фотобанка...")
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
