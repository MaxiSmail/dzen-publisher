import sys
import time
from playwright.sync_api import sync_playwright
from config import BROWSER_DATA_DIR

def run_login():
    print("=" * 60)
    print("=== АВТОРИЗАЦИЯ В INSTAGRAM ===")
    print("=" * 60)
    print(f"Данные сессии будут сохранены в:\n{BROWSER_DATA_DIR}\n")
    print("Сейчас откроется окно браузера.")
    print("1. Введите логин и пароль в Instagram.")
    print("2. Если включена двухфакторная аутентификация — введите код.")
    print("3. Нажмите 'Сохранить данные для входа' (Save info), если появится предложение.")
    print("4. Когда вы увидите главную страницу Instagram или директ, вернитесь сюда и нажмите Enter.")
    print("=" * 60)

    BROWSER_DATA_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_DATA_DIR),
            headless=False,
            viewport={"width": 1280, "height": 800},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )

        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://www.instagram.com/", wait_until="domcontentloaded")

        try:
            input("\n>>> Нажмите ENTER здесь, когда успешно войдете в аккаунт... ")
        except (EOFError, KeyboardInterrupt):
            print("\nЗавершение...")

        # Небольшая пауза для сохранения cookies
        time.sleep(2)
        context.close()
        print("\n[OK] Сессия успешно сохранена! Теперь можно запускать сбор сообщений.")

if __name__ == "__main__":
    run_login()
