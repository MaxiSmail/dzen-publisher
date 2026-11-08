import json
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent
USER_DATA_DIR = Path("C:/Users/maksi/.dzen_profile")
OUTPUT_FILE = BASE_DIR / "github_session_secret.txt"

print(f"Экспорт сессии из: {USER_DATA_DIR}")

try:
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        storage_state = context.storage_state()
        storage_json = json.dumps(storage_state, ensure_ascii=False)
        b64_state = base64.b64encode(storage_json.encode('utf-8')).decode('utf-8')
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(b64_state)
            
        context.close()
        print("Сессия успешно сохранена в github_session_secret.txt")
except Exception as e:
    print(f"Ошибка при экспорте: {e}")