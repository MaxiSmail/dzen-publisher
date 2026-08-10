import sys
import json
import argparse
import feedparser
from bs4 import BeautifulSoup
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import config
import brain
import image_gen
import publisher

def load_history() -> list:
    if config.HISTORY_FILE.exists():
        try:
            with open(config.HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка чтения истории публикаций VK: {e}")
            return []
    return []

def save_history(history: list):
    try:
        with open(config.HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения истории публикаций VK: {e}")

def clean_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def run_mode_own_rss():
    print("\n--- ЗАПУСК УТРЕННЕЙ СОБСТВЕННОЙ ПУБЛИКАЦИИ VK ПО RSS ---")
    history = load_history()
    
    selected_article = None
    for feed_url in config.RSS_FEEDS:
        print(f"Парсинг RSS-ленты: {feed_url}...")
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                link = entry.get("link", "")
                if not link or link in history:
                    continue
                
                title = entry.get("title", "")
                summary_raw = entry.get("summary", "") or entry.get("description", "")
                content_clean = clean_html(summary_raw)
                
                selected_article = {
                    "title": title,
                    "link": link,
                    "content": content_clean[:3000]
                }
                print(f"Найдена свежая статья для VK: '{title}' ({link})")
                break
        except Exception as e:
            print(f"Ошибка при парсинге {feed_url}: {e}")
            
        if selected_article:
            break
            
    if not selected_article:
        print("Свежих необработанных новостей для VK не найдено.")
        return
        
    # Генерация поста
    try:
        post_data = brain.generate_post_from_rss(selected_article)
    except Exception as e:
        print(f"ИИ-генерация VK-поста провалилась: {e}")
        return
        
    # Генерация обложки (с автоматическим фоллбеком)
    try:
        image_path, _ = image_gen.generate_image(post_data["image_prompt"])
    except Exception as e:
        print(f"Ошибка вызова генератора обложки: {e}")
        image_path = None
        
    # Публикация
    success = publisher.publish_to_vk(post_data["formatted_text"], image_path)
    if success:
        history.append(selected_article["link"])
        save_history(history)
        
        # Удаляем временную картинку
        if image_path and Path(image_path).exists():
            try:
                Path(image_path).unlink()
            except:
                pass
        print("Утренняя публикация VK успешно завершена!")

def run_mode_dzen_adaptation():
    print("\n--- ЗАПУСК ДНЕВНОЙ АДАПТАЦИИ СТАТЬИ ДЗЕНА ДЛЯ VK ---")
    history = load_history()
    
    print(f"Парсинг RSS-ленты Дзен-канала: {config.DZEN_CHANNEL_RSS}...")
    try:
        feed = feedparser.parse(config.DZEN_CHANNEL_RSS)
    except Exception as e:
        print(f"Ошибка парсинга RSS Дзена: {e}")
        return
        
    if not feed.entries:
        print("Лента Дзен пуста или недоступна.")
        return
        
    latest_entry = feed.entries[0]
    link = latest_entry.get("link", "")
    title = latest_entry.get("title", "")
    summary_raw = latest_entry.get("summary", "") or latest_entry.get("description", "") or latest_entry.get("content", "")
    
    if link in history:
        print(f"Последняя статья Дзена '{title}' ({link}) уже опубликована в VK.")
        return
        
    content_clean = clean_html(summary_raw)
    
    print(f"Обнаружена новая статья в Дзене для адаптации: '{title}'")
    
    # Адаптация поста
    try:
        post_data = brain.adapt_dzen_article_to_vk(title, content_clean[:3000])
    except Exception as e:
        print(f"ИИ-адаптация статьи Дзена провалилась: {e}")
        return
        
    # Генерация обложки
    try:
        image_path, _ = image_gen.generate_image(post_data["image_prompt"])
    except Exception as e:
        print(f"Ошибка вызова генератора обложки: {e}")
        image_path = None
        
    # Публикация
    success = publisher.publish_to_vk(post_data["formatted_text"], image_path)
    if success:
        history.append(link)
        save_history(history)
        
        # Удаляем временную картинку
        if image_path and Path(image_path).exists():
            try:
                Path(image_path).unlink()
            except:
                pass
        print("Публикация адаптированной статьи Дзена во ВКонтакте успешно завершена!")

def main():
    parser = argparse.ArgumentParser(description="Автопостинг сообщества ВКонтакте на базе ИИ")
    parser.add_argument(
        "--mode", 
        choices=["own_rss", "dzen_adaptation"], 
        required=True, 
        help="Режим работы: own_rss (утренняя статья по RSS) или dzen_adaptation (дневная адаптация Дзен)"
    )
    args = parser.parse_args()
    
    if args.mode == "own_rss":
        run_mode_own_rss()
    elif args.mode == "dzen_adaptation":
        run_mode_dzen_adaptation()

if __name__ == "__main__":
    main()
