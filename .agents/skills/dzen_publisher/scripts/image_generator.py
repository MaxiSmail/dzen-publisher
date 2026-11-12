import urllib.parse
import requests
import random
import time
from pathlib import Path
import config

def generate_and_download_image(prompt: str, filename_prefix: str = "cover") -> Path:
    """
    Генератор фотореалистичных обложек для Дзена в журнальном стиле (FLUX).
    Исключает дешевый пластиковый ИИ-стиль (неон, роботы, 3D-рендеры).
    """
    print(f"Генерация редакционной обложки (FLUX): '{prompt[:70]}...'")
    
    # Добавляем модификаторы кинематографичной фотографии и жесткие негативные фильтры
    enhanced_prompt = (
        f"{prompt}. Shot on 35mm film, Leica M11 photography, 50mm f/1.4 lens, "
        f"natural soft daylight, authentic textures, documentary aesthetic, rich colors. "
        f"Avoid: 3d render, cgi, cartoon, neon glow, blue holograms, glowing circuits, "
        f"robot faces, cyberpunk, plastic skin, distorted hands, text, typography, watermark"
    )
    
    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    seed = random.randint(1, 1000000)
    output_path = config.IMAGE_DIR / f"{filename_prefix}_{seed}.jpg"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    # Каскад фотореалистичных движков на базе FLUX (без пластикового турбо-мыла)
    engines = [
        ("Pollinations FLUX", f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=675&model=flux&nologo=true&seed={seed}"),
        ("Pollinations FLUX-Realism", f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=675&model=flux-realism&nologo=true&seed={seed}")
    ]
    
    for engine_name, url in engines:
        try:
            print(f"Попытка генерации через {engine_name}...")
            response = requests.get(url, headers=headers, timeout=45)
            if response.status_code == 200 and len(response.content) > 10000:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Премиальная обложка успешно сгенерирована ({len(response.content)} байт): {output_path}")
                return output_path
            else:
                print(f"⚠️ {engine_name} вернул статус: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Ошибка {engine_name}: {e}")
        time.sleep(1)
        
    # Резервный источник: если движки перегружены, берем качественное фото из проверенного источника
    print("⚠️ Генераторы перегружены. Загрузка из фотобанка...")
    fallback_url = "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&h=675&q=80"
    try:
        res = requests.get(fallback_url, headers=headers, timeout=20)
        if res.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(res.content)
            return output_path
    except Exception as e:
        print(f"Ошибка загрузки фотобанка: {e}")
        
    raise RuntimeError("Не удалось сгенерировать качественную обложку")

if __name__ == "__main__":
    test_prompt = "Close-up of modern minimalist designer desk with laptop, notebook and cup of coffee in morning sun"
    try:
        p = generate_and_download_image(test_prompt, "test")
        print("Тест пройден:", p.exists())
    except Exception as e:
        print("Ошибка:", e)
