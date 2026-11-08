import json
import time
from pathlib import Path
from typing import Dict, List, Optional
import config

ANALYTICS_FILE = config.BASE_DIR / "analytics_history.json"

def load_analytics_history() -> List[Dict]:
    if ANALYTICS_FILE.exists():
        try:
            with open(ANALYTICS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка чтения аналитики: {e}")
            return []
    return []

def save_analytics_history(data: List[Dict]):
    try:
        with open(ANALYTICS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения аналитики: {e}")

def record_post_event(title: str, tags: List[str], link: str):
    """Фиксирует факт нового поста для отслеживания динамики."""
    history = load_analytics_history()
    event = {
        "timestamp": int(time.time()),
        "title": title,
        "tags": tags,
        "link": link,
        "views": 0,
        "forwards": 0
    }
    history.append(event)
    save_analytics_history(history)
    print("Данные публикации сохранены в аналитический модуль SMM.")

def get_top_performing_topics() -> str:
    """Возвращает рекомендательный контекст на основе накопленной аналитики."""
    history = load_analytics_history()
    if not history:
        return "Рекомендации SMM: Пока мало данных. Фокусируйся на ярких практических гайдах по ИИ 2026 года."
        
    tag_counts = {}
    for item in history:
        for tag in item.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_tags_str = ", ".join([f"#{t[0]}" for t in sorted_tags]) if sorted_tags else "#нейросети, #технологии"
    
    return f"Рекомендации СММ-директора: Самый высокий отклик аудитории вызывают посты по тегам: {top_tags_str}. Сделай акцент на них!"

if __name__ == "__main__":
    print(get_top_performing_topics())
