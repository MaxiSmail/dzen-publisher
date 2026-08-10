import time
from playwright.sync_api import sync_playwright
import config

def dump_dom():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(config.USER_DATA_DIR),
            headless=True,
            args=["--no-sandbox"]
        )
        page = context.new_page()
        
        print("Переход в Дзен-студию...")
        page.goto("https://dzen.ru/studio", wait_until="networkidle", timeout=60000)
        time.sleep(5)
        
        # Открываем меню профиля
        avatar = page.locator('[class*="avatar"], [class*="profile"], header img').first
        avatar.click()
        time.sleep(2)
        
        # Кликаем "Создать публикацию"
        page.get_by_text("Создать публикацию").first.click()
        time.sleep(2)
        
        # Кликаем "Написать статью"
        page.get_by_text("Написать статью").first.click()
        time.sleep(6)
        
        # Закрываем приветственный модал
        page.keyboard.press("Escape")
        time.sleep(1)
        
        # Сохраняем полный DOM в файл
        html_content = page.content()
        with open("editor_dom.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("DOM редактора успешно сохранен в editor_dom.html")
        
        # Ищем все теги input
        inputs = page.locator("input").all()
        print(f"\nНайдено полей ввода (input): {len(inputs)}")
        for idx, inp in enumerate(inputs):
            try:
                type_attr = inp.get_attribute("type") or "text"
                class_attr = inp.get_attribute("class") or ""
                id_attr = inp.get_attribute("id") or ""
                accept_attr = inp.get_attribute("accept") or ""
                print(f"Input {idx} | Type: {type_attr} | ID: {id_attr} | Class: {class_attr} | Accept: {accept_attr}")
            except:
                pass
                
        # Ищем все кнопки и иконки на панели редактора
        buttons = page.locator("button, [role='button']").all()
        print(f"\nНайдено кнопок/элементов управления: {len(buttons)}")
        for idx, btn in enumerate(buttons[:30]):
            try:
                text = btn.inner_text().strip()
                title = btn.get_attribute("title") or ""
                class_name = btn.get_attribute("class") or ""
                html = btn.evaluate("el => el.outerHTML")[:120]
                if text or title:
                    print(f"Кнопка {idx} | Текст: '{text}' | Title: '{title}' | Class: '{class_name}' | HTML: {html}")
            except:
                pass
                
        context.close()

if __name__ == "__main__":
    dump_dom()
