import sys
from playwright.sync_api import sync_playwright
import config

def run_login():
    print("=" * 60)
    print("ЗАПУСК ПОМОЩНИКА АВТОРИЗАЦИИ ДЗЕН")
    print("=" * 60)
    print(f"Путь к профилю браузера: {config.USER_DATA_DIR}")
    print("Сейчас откроется окно браузера. Пожалуйста:")
    print("1. Войдите в свой аккаунт Яндекс / Дзен.")
    print("2. Пройдите проверку безопасности (SMS, капчу, если потребуется).")
    print("3. Убедитесь, что вы находитесь в Дзен-студии (dzen.ru/studio).")
    print("4. После этого вернитесь в эту консоль и нажмите ENTER, чтобы сохранить сессию.")
    print("=" * 60)

    with sync_playwright() as p:
        # Запускаем браузер с постоянным профилем
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(config.USER_DATA_DIR),
            headless=False,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled", # Снижает вероятность обнаружения робота
                "--start-maximized"
            ],
            no_viewport=True
        )
        
        page = context.new_page()
        page.goto("https://dzen.ru/studio")
        
        input("\nНажмите ENTER здесь, когда успешно авторизуетесь и будете готовы закрыть браузер...")
        
        print("Закрытие браузера и сохранение сессии...")
        context.close()
        print("Сессия сохранена успешно!")

if __name__ == "__main__":
    run_login()
