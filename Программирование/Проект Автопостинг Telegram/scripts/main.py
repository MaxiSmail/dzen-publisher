import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import parser
import brain
import image_gen
import publisher
import analytics

def run_autopilot():
    print("=" * 60)
    print("ЗАПУСК АВТОНОМНОГО Telegram-ПОСТИНГА")
    print("=" * 60)
    
    # 1. Сбор свежей необработанной новости
    article = parser.fetch_latest_unposted_article()
    if not article:
        print("Завершение работы: свежих новостей не найдено.")
        return
        
    print(f"\n[1/4] Обработка новости: {article['title']}")
    
    # 2. ИИ генерация текста поста и промпта картинки через Gemini
    try:
        post_data = brain.generate_post_from_article(article)
    except Exception as e:
        print(f"Ошибка на этапе ИИ-генерации: {e}")
        return
        
    print("\n[2/4] Текст поста сгенерирован.")
    
    # 3. Генерация обложки для поста
    try:
        image_path, image_url = image_gen.generate_image(post_data["image_prompt"])
    except Exception as e:
        print(f"Ошибка генерации картинки: {e}")
        return
        
    print("\n[3/4] Изображение сгенерировано.")
    
    # 4. Публикация в Telegram
    success = publisher.publish_to_telegram(post_data["formatted_text"], image_path, image_url=image_url)
    
    if success:
        # Сохраняем ссылку на новость в историю и фиксируем событие аналитики СММ
        history = parser.load_history()
        history.append(article["link"])
        parser.save_history(history)
        
        analytics.record_post_event(post_data.get("title", ""), post_data.get("tags", []), article["link"])
        print("\n[4/4] Цикл завершен успешно! Новость опубликована и учтена в аналитике СММ.")
    else:
        print("\nОшибка на этапе публикации.")

if __name__ == "__main__":
    run_autopilot()
