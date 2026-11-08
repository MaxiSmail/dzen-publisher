import sys
import os
import json
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright
import config

def run_login():
    print("=" * 60)
    print("ЗАПУСК ПОМОЩНИКА АВТОРИЗАЦИИ ДЗЕН")
    print("=" * 60)
    print(f"Путь к профилю браузера: {config.USER_DATA_DIR}")
    print("\nСейчас откроется окно браузера.")
    print("1. Войдите в свой аккаунт Яндекс / Дзен.")
    print("2. Пройдите проверку безопасности (SMS / пуш, если потребуется).")
    print("3. Убедитесь, что вы находитесь в Дзен-студии (dzen.ru/studio).")
    print("4. После этого вернитесь в это окно и нажмите ENTER.")
    print("=" * 60)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(config.USER_DATA_DIR),
            headless=False,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ],
            no_viewport=True
        )
        
        page = context.new_page()
        page.goto("https://dzen.ru/studio")
        
        input("\n>>> Нажмите ENTER здесь, когда успешно авторизуетесь в студии: ")
        
        # Получаем cookies и storage
        storage_state = context.storage_state()
        storage_json = json.dumps(storage_state, ensure_ascii=False)
        b64_state = base64.b64encode(storage_json.encode('utf-8')).decode('utf-8')
        
        output_file = config.BASE_DIR / "github_session_secret.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(b64_state)
        print(f"\nСессия успешно сохранена в файл: {output_file}")
        
        print("\nЗакрытие браузера...")
        context.close()
        print("Готово!")

if __name__ == "__main__":
    run_login()
