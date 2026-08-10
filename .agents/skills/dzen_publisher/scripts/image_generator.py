import urllib.parse
import requests
import random
from pathlib import Path
import config

def generate_and_download_image(prompt: str, filename_prefix: str = "cover") -> Path:
    print(f"Генерация обложки для промпта: '{prompt}'...")
    
    # URL-кодируем промпт
    encoded_prompt = urllib.parse.quote(prompt)
    
    # Генерируем случайный seed для разнообразия картинок
    seed = random.randint(1, 1000000)
    
    # Используем Pollinations.ai (бесплатный стабильный генератор картинок Flux)
    # nologo=true убирает ватермарку, seed дает разнообразие
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&nologo=true&seed={seed}"
    
    output_path = config.IMAGE_DIR / f"{filename_prefix}_{seed}.jpg"
    
    try:
        response = requests.get(image_url, timeout=45)
        response.raise_for_status()
        
        # Сохраняем картинку
        with open(output_path, "wb") as f:
            f.write(response.content)
            
        print(f"Обложка успешно сгенерирована и сохранена в: {output_path}")
        return output_path
    except Exception as e:
        print(f"Ошибка при генерации или скачивании изображения: {e}")
        # Если генерация не сработала, вернем None или сгенерируем дефолтную ошибку
        raise e

if __name__ == "__main__":
    # Тестовый запуск
    test_prompt = "A high-quality 3D render of a futuristic quantum computer glowing in the dark, science fiction style, highly detailed"
    try:
        path = generate_and_download_image(test_prompt, "test")
        print(f"Тест пройден. Картинка сохранена: {path.exists()}")
    except Exception as e:
        print(f"Тест провален: {e}")
