import os
import time
import base64
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
import config

CHANNEL_ID = "623c51ed88b1104ddc4eb738"
BASE_STUDIO_URL = f"https://dzen.ru/profile/editor/id/{CHANNEL_ID}"

def collect_analytics() -> dict:
    print("=" * 60)
    print("МОДУЛЬ АНАЛИТИКИ КАНАЛА (ПРЯМОЙ ДОСТУП К МЕТРИКАМ)")
    print("=" * 60)
    
    session_secret_b64 = os.environ.get("DZEN_SESSION_STATE")
    storage_state_path = None
    
    if session_secret_b64:
        try:
            decoded_json = base64.b64decode(session_secret_b64.encode('utf-8')).decode('utf-8')
            storage_state_path = config.BASE_DIR / "temp_storage_state.json"
            with open(storage_state_path, "w", encoding="utf-8") as f:
                f.write(decoded_json)
        except Exception as err:
            print(f"Ошибка декодирования DZEN_SESSION_STATE в аналитике: {err}")

    if not storage_state_path and not config.USER_DATA_DIR.exists():
        print("Ошибка: профиль браузера не найден.")
        return {}

    metrics_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "published_count": 0,
        "statistics_summary": "",
        "monetization_summary": "",
        "recommendations": []
    }

    with sync_playwright() as p:
        if storage_state_path:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                storage_state=str(storage_state_path),
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            )
        else:
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(config.USER_DATA_DIR),
                headless=True,
                args=["--no-sandbox"]
            )
        page = context.new_page()
        
        try:
            print("1. Переход в статистику публикаций...")
            stats_url = f"{BASE_STUDIO_URL}/publications-stat"
            page.goto(stats_url, wait_until="networkidle", timeout=60000)
            time.sleep(4)
            
            stats_screenshot = config.BASE_DIR / "analytics_stats.png"
            page.screenshot(path=str(stats_screenshot))
            
            stats_text = page.locator('body').inner_text()
            metrics_data["statistics_summary"] = stats_text[:1500]
            
            print("2. Переход в раздел Монетизация...")
            money_url = f"{BASE_STUDIO_URL}/money"
            page.goto(money_url, wait_until="networkidle", timeout=60000)
            time.sleep(4)
            
            money_screenshot = config.BASE_DIR / "analytics_monetization.png"
            page.screenshot(path=str(money_screenshot))
            
            money_text = page.locator('body').inner_text()
            metrics_data["monetization_summary"] = money_text[:1500]
            
            recommendations = []
            if "0" in stats_text or "нет данных" in stats_text.lower() or "мало" in stats_text.lower():
                recommendations.append("Канал имеет низкие охваты: усиливаем интригу в заголовках и делаем упор на темы заработка/применения ИИ.")
            
            recommendations.append("Добавлять готовые промпты и пошаговые инструкции в каждую статью для увеличения дочитываний.")
            metrics_data["recommendations"] = recommendations
            
            analytics_log_file = config.BASE_DIR / "analytics_history.json"
            history = []
            if analytics_log_file.exists():
                try:
                    with open(analytics_log_file, "r", encoding="utf-8") as f:
                        history = json.load(f)
                except:
                    history = []
                    
            history.append(metrics_data)
            with open(analytics_log_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
                
            print("АНАЛИЗ КАНАЛА ЗАВЕРШЕН УСПЕШНО!")
            
            if storage_state_path and storage_state_path.exists():
                try:
                    storage_state_path.unlink()
                except:
                    pass

            context.close()
            return metrics_data

        except Exception as err:
            print(f"Ошибка сбора аналитики: {err}")
            context.close()
            return metrics_data

if __name__ == "__main__":
    collect_analytics()
