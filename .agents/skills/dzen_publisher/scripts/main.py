import sys
import json
import time
import random
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import config
import agent_brain
import image_generator
import publisher
import analytics
import telegram_notifier

def main():
    print("=" * 60)
    print("ЗАПУСК ДЗЕН-АГЕНТА: ИИ-ДИРЕКТОР КАНАЛА (С TELEGRAM УВЕДОМЛЕНИЯМИ)")
    print("=" * 60)
    
    if "--random-delay" in sys.argv:
        delay_minutes = random.randint(2, 35)
        print(f"Имитация естественного графика человека: выдерживаем паузу {delay_minutes} мин. перед открытием браузера...")
        time.sleep(delay_minutes * 60)
    
    # 1. Проверяем наличие ключа Gemini API (считывается как из .env, так и напрямую из Secrets на GitHub)
    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == "your_gemini_api_key_here":
        print("Ошибка: GEMINI_API_KEY не установлен!")
        sys.exit(1)

    # 2. Сбор аналитики
    print("\n--- ЭТАП 1: СБОР И АНАЛИЗ СТАТИСТИКИ КАНАЛА ---")
    analytics_data = {}
    try:
        analytics_data = analytics.collect_analytics()
    except Exception as e:
        print(f"Не удалось собрать аналитику (продолжаем в стандартном режиме): {e}")

    # 3. Генерация статьи
    print("\n--- ЭТАП 2: АДАПТИВНАЯ ГЕНЕРАЦИЯ СТАТЬИ ---")
    try:
        article_data = agent_brain.generate_article(analytics_data=analytics_data)
    except Exception as e:
        print(f"Критическая ошибка при генерации статьи: {e}")
        sys.exit(1)
        
    # 4. Генерация обложки
    print("\n--- ЭТАП 3: ГЕНЕРАЦИЯ ОБЛОЖКИ ---")
    image_path = None
    if "image_prompt" in article_data and article_data["image_prompt"]:
        try:
            image_path = image_generator.generate_and_download_image(
                article_data["image_prompt"],
                filename_prefix="dzen_cover"
            )
        except Exception as e:
            print(f"Не удалось сгенерировать изображение (продолжаем без обложки): {e}")
            
    # 5. Архивация
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    archive_file = config.ARCHIVE_DIR / f"post_{timestamp}.json"
    archive_data = {
        "timestamp": timestamp,
        "article": article_data,
        "analytics_data": analytics_data,
        "image_path": str(image_path) if image_path else None
    }
    with open(archive_file, "w", encoding="utf-8") as f:
        json.dump(archive_data, f, indent=2, ensure_ascii=False)
    print(f"Резервная копия статьи сохранена в архив: {archive_file}")
    
    # 6. Публикация
    print("\n--- ЭТАП 4: ЧЕЛОВЕЧЕСКАЯ ПУБЛИКАЦИЯ В ДЗЕН ---")
    success = publisher.publish_to_dzen(article_data, image_path=image_path, headless=True)
    
    if success:
        print("\n" + "=" * 60)
        print("ПРОЦЕСС ПУБЛИКАЦИИ УСПЕШНО ЗАВЕРШЕН!")
        print("=" * 60)
        
        # 7. Отправка Telegram уведомления
        screenshot_path = config.BASE_DIR / "latest_publication.png"
        telegram_notifier.send_telegram_notification(
            title=article_data["title"],
            tags=article_data.get("tags", []),
            screenshot_path=screenshot_path
        )
        
        if image_path and image_path.exists():
            try:
                image_path.unlink()
            except:
                pass
    else:
        print("\nПроизошла ошибка при публикации в Дзен. Проверьте логи и скриншот ошибки.")
        sys.exit(1)

if __name__ == "__main__":
    main()
