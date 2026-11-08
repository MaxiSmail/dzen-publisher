import json
import feedparser
from bs4 import BeautifulSoup
from typing import Optional, Dict
import config

def load_history() -> list:
    if config.HISTORY_FILE.exists():
        try:
            with open(config.HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка чтения истории: {e}")
            return []
    return []

def save_history(history: list):
    try:
        with open(config.HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения истории: {e}")

def clean_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def fetch_latest_unposted_article() -> Optional[Dict[str, str]]:
    history = load_history()
    
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
                
                print(f"Найдена свежая статья: '{title}' ({link})")
                return {
                    "title": title,
                    "link": link,
                    "content": content_clean[:3000] # Берем до 3000 символов
                }
        except Exception as e:
            print(f"Ошибка при парсинге {feed_url}: {e}")
            
    print("Новых необработанных статей не найдено.")
    return None

if __name__ == "__main__":
    article = fetch_latest_unposted_article()
    if article:
        print("Успех:", article["title"])
    else:
        print("Ничего не найдено.")
