import os
import time
import random
import base64
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError
import config

def type_humanlike(page, text: str):
    """
    Симулирует естественную печать живого человека:
    вводит слова с плавающими задержками клавиш (10-35 мс) и делает паузы на знаках препинания.
    """
    words = text.split(" ")
    for idx, word in enumerate(words):
        token = word + (" " if idx < len(words) - 1 else "")
        page.keyboard.type(token, delay=random.randint(10, 35))
        
        if word.endswith((",", ".", "!", "?", ";", ":")):
            time.sleep(random.uniform(0.2, 0.6))
        elif random.random() < 0.12:
            time.sleep(random.uniform(0.15, 0.45))

def publish_to_dzen(article_data: dict, image_path: Path = None, headless: bool = True) -> bool:
    print("=" * 60)
    print("НАЧАЛО ПУБЛИКАЦИИ В ДЗЕН (ИИ-ДИРЕКТОР КАНАЛА)")
    print("=" * 60)
    
    # Поддержка гибридного режима авторизации (Локальный профиль или GitHub Secrets)
    session_secret_b64 = os.environ.get("DZEN_SESSION_STATE")
    storage_state_path = None
    
    if session_secret_b64:
        print("Обнаружен облачный секрет авторизации DZEN_SESSION_STATE (GitHub Actions Mode)!")
        try:
            decoded_json = base64.b64decode(session_secret_b64.encode('utf-8')).decode('utf-8')
            storage_state_path = config.BASE_DIR / "temp_storage_state.json"
            with open(storage_state_path, "w", encoding="utf-8") as f:
                f.write(decoded_json)
        except Exception as err:
            print(f"Ошибка декодирования DZEN_SESSION_STATE: {err}")

    if not storage_state_path and not config.USER_DATA_DIR.exists():
        print("Ошибка: профиль авторизации не найден!")
        return False

    with sync_playwright() as p:
        print("Запуск браузера...")
        if storage_state_path:
            browser = p.chromium.launch(
                headless=headless,
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                storage_state=str(storage_state_path),
                permissions=["clipboard-read", "clipboard-write"],
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            )
        else:
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(config.USER_DATA_DIR),
                headless=headless,
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled", "--start-maximized"],
                no_viewport=True,
                permissions=["clipboard-read", "clipboard-write"]
            )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        try:
            print("1. Переход в Студию Дзена...")
            page.goto("https://dzen.ru/profile/editor/neuro_hacks_ai", wait_until="domcontentloaded", timeout=60000)
            time.sleep(random.uniform(3.0, 5.0))
            page.keyboard.press("Escape")
            time.sleep(1.0)
            
            print("2. Открываем меню добавления публикации...")
            add_btn = page.locator('[class*="addButton"]').first
            add_btn.wait_for(state="visible", timeout=15000)
            add_btn.click()
            time.sleep(1.5)
            
            print("3. Выбираем 'Написать статью'...")
            art_btn = page.locator('text="Написать статью"').first
            art_btn.wait_for(state="visible", timeout=15000)
            art_btn.click()
            
            print("4. Ожидаем загрузку редактора...")
            page.wait_for_selector('[contenteditable="true"]', timeout=30000)
            time.sleep(3.0)
            page.keyboard.press("Escape") # закрываем онбординг подсказку
            time.sleep(1.0)
            
            print("5. Ввод заголовка статьи...")
            title_element = page.locator('[contenteditable="true"]').first
            title_element.click()
            time.sleep(0.5)
            type_humanlike(page, article_data["title"])
            print(f"Заголовок успешно набран: '{article_data['title']}'")
            time.sleep(1.5)
            
            print("6. Фокусируемся на текстовом поле...")
            body_element = page.locator('[contenteditable="true"]').nth(1)
            body_element.click()
            time.sleep(1.0)
            
            # Вставка обложки статьи через нативный файловый загрузчик Дзена
            if image_path and Path(image_path).exists():
                print(f"Загрузка обложки статьи: {image_path}...")
                try:
                    side_btn = page.locator('[class*="side-button__sideButton"]').first
                    if side_btn.is_visible(timeout=5000):
                        side_btn.click()
                        time.sleep(1.0)
                        file_btn = page.locator('[class*="image-popup__fileButton"]').first
                        with page.expect_file_chooser(timeout=8000) as fc_info:
                            file_btn.click()
                        fc = fc_info.value
                        fc.set_files(str(Path(image_path).resolve()))
                        print("Обложка передана в загрузчик Дзена. Ожидание завершения отгрузки на сервер...")
                        time.sleep(6.0)
                        print("Обложка успешно встроена в статью!")
                        page.keyboard.press("Enter")
                        time.sleep(1.0)
                except Exception as img_err:
                    print(f"Предупреждение: Ошибка вставки обложки: {img_err}")
            
            paragraphs = [p.strip() for p in article_data["content"].split("\n") if p.strip()]
            print(f"Всего абзацев для набора: {len(paragraphs)}")
            
            for idx, paragraph in enumerate(paragraphs):
                is_heading = paragraph.isupper() and len(paragraph) < 80 and not paragraph.endswith(".")
                
                if is_heading:
                    print(f"Печать подзаголовка H2: '{paragraph}'...")
                    page.keyboard.press("Control+B")
                    time.sleep(0.2)
                    type_humanlike(page, paragraph)
                    time.sleep(0.2)
                    page.keyboard.press("Control+B")
                else:
                    type_humanlike(page, paragraph)
                    
                page.keyboard.press("Enter")
                time.sleep(random.uniform(0.3, 0.6))

            print("Набор текста статьи успешно завершен!")
            time.sleep(2.0)
            
            print("7. Поиск кнопки 'Опубликовать'...")
            publish_btn = page.locator('button:has-text("Опубликовать")').first
            publish_btn.wait_for(state="visible", timeout=15000)
            publish_btn.click()
            print("Нажата первая кнопка публикации...")
            time.sleep(3.0)
            
            if "tags" in article_data and article_data["tags"]:
                print(f"Добавление тегов: {article_data['tags']}...")
                try:
                    tags_input = page.locator('input[placeholder*="Тег"], input[placeholder*="тег"]').first
                    if tags_input.is_visible(timeout=5000):
                        tags_input.click()
                        time.sleep(0.5)
                        for tag in article_data["tags"]:
                            type_humanlike(page, tag)
                            time.sleep(0.4)
                            page.keyboard.press("Enter")
                            time.sleep(0.4)
                        print("Теги успешно добавлены.")
                except Exception as tag_err:
                    print(f"Теги пропущены: {tag_err}")
            
            print("8. Нажатие финальной кнопки публикации...")
            final_publish_btn = page.locator('button:has-text("Опубликовать")').last
            final_publish_btn.wait_for(state="visible", timeout=15000)
            time.sleep(1.5)
            final_publish_btn.click()
            print("Финальная кнопка публикации нажата!")
            
            time.sleep(6.0)
            print("Публикация успешно завершена!")
            
            screenshot_path = config.BASE_DIR / "latest_publication.png"
            page.screenshot(path=str(screenshot_path))
            print(f"Скриншот публикации сохранен в: {screenshot_path}")
            
            if storage_state_path and storage_state_path.exists():
                try:
                    storage_state_path.unlink()
                except:
                    pass

            context.close()
            return True
            
        except TimeoutError as te:
            print(f"Превышено время ожидания элементов интерфейса: {te}")
            err_screenshot = config.BASE_DIR / "error_screenshot.png"
            page.screenshot(path=str(err_screenshot))
            context.close()
            return False
        except Exception as e:
            print(f"Критическая ошибка при публикации: {e}")
            err_screenshot = config.BASE_DIR / "error_screenshot.png"
            try:
                page.screenshot(path=str(err_screenshot))
            except:
                pass
            context.close()
            return False
