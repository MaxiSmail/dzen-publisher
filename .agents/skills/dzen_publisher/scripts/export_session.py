import json
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright
import config

def export_session():
    print("=" * 60)
    print("ЭКСПОРТ СЕССИИ ДЗЕНА ДЛЯ GITHUB ACTIONS")
    print("=" * 60)
    
    if not config.USER_DATA_DIR.exists():
        print("Ошибка: профиль браузера не найден! Сначала авторизуйтесь через login.bat.")
        return

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(config.USER_DATA_DIR),
            headless=True,
            args=["--no-sandbox"]
        )
        
        # Сохраняем состояния cookies и storage
        storage_state = context.storage_state()
        storage_json = json.dumps(storage_state, ensure_ascii=False)
        
        # Кодируем в Base64 для удобной вставки в GitHub Secrets
        b64_state = base64.b64encode(storage_json.encode('utf-8')).decode('utf-8')
        
        output_file = config.BASE_DIR / "github_session_secret.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(b64_state)
            
        print("\nУСПЕШНО!")
        print(f"Зашифрованный ключ сессии сохранен в файл: {output_file}")
        print("Скопируйте содержимое этого файла и вставьте в GitHub Secrets с именем DZEN_SESSION_STATE.")
        context.close()

if __name__ == "__main__":
    export_session()
