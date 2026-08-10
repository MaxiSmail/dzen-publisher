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

def publish_to_dzen(article_data: dict, image_path: Path = None, headless: bool = False) -> bool:
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
        print("Запустите login.bat или добавьте DZEN_SESSION_STATE в Secrets.")
        return False

    with sync_playwright() as p:
        print("Запуск браузера...")
        if storage_state_path:
            # Запуск в облачном режиме через storage_state
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
            # Локальный запуск через persistent context
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(config.USER_DATA_DIR),
                headless=headless,
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled", "--start-maximized"],
                no_viewport=True,
                permissions=["clipboard-read", "clipboard-write"]
            )
        
        page = context.new_page()
        
        try:
            print("Переход в Дзен-студию...")
            page.goto("https://dzen.ru/studio", wait_until="domcontentloaded", timeout=60000)
            time.sleep(random.uniform(4.0, 7.0))
            
            print("Дзен-студия загружена. Проверяем сессию...")
            avatar_selector = '[class*="avatar"], [class*="profile"], header img, .header__avatar'
            avatar = page.locator(avatar_selector).first
            
            try:
                avatar.wait_for(state="visible", timeout=15000)
                print("Сессия активна (аватарка профиля найдена).")
            except Exception:
                print("Ошибка: аватарка не найдена. Сессия устарела.")
                context.close()
                return False
                
            print("Кликаем по аватарке профиля...")
            avatar.click()
            time.sleep(random.uniform(1.5, 3.0))
            
            print("Кликаем по кнопке 'Создать публикацию'...")
            create_pub_btn = page.get_by_text("Создать публикацию").first
            create_pub_btn.wait_for(state="visible", timeout=10000)
            create_pub_btn.click()
            time.sleep(random.uniform(1.5, 2.5))
            
            print("Кликаем по пункту 'Написать статью'...")
            article_btn = page.get_by_text("Написать статью").first
            article_btn.wait_for(state="visible", timeout=10000)
            article_btn.click()
            print("Выбран пункт 'Написать статью'. Ожидание загрузки редактора...")
            time.sleep(random.uniform(5.0, 8.0))
            
            print("Закрытие приветственных окон...")
            page.keyboard.press("Escape")
            time.sleep(random.uniform(1.5, 2.5))
            
            print("Ввод заголовка статьи...")
            title_element = page.locator('[contenteditable="true"]').first
            title_element.wait_for(state="visible", timeout=15000)
            title_element.click()
            time.sleep(random.uniform(0.5, 1.2))
            
            type_humanlike(page, article_data["title"])
            print(f"Заголовок успешно набран: '{article_data['title']}'")
            time.sleep(random.uniform(1.5, 3.0))
            
            print("Фокусируемся на текстовом поле...")
            body_element = page.locator('[contenteditable="true"]').nth(1)
            body_element.wait_for(state="visible", timeout=15000)
            body_element.focus()
            time.sleep(random.uniform(1.0, 2.0))
            
            paragraphs = [p.strip() for p in article_data["content"].split("\n") if p.strip()]
            print(f"Всего абзацев для набора: {len(paragraphs)}")
            
            for idx, paragraph in enumerate(paragraphs):
                is_heading = paragraph.isupper() and len(paragraph) < 80 and not paragraph.endswith(".")
                
                if is_heading:
                    print(f"Печать подзаголовка H2: '{paragraph}'...")
                    page.keyboard.press("Control+B")
                    time.sleep(0.3)
                    type_humanlike(page, paragraph)
                    time.sleep(0.3)
                    page.keyboard.press("Control+B")
                else:
                    print(f"Человеческий набор абзаца {idx+1}/{len(paragraphs)}...")
                    type_humanlike(page, paragraph)
                
                time.sleep(random.uniform(0.8, 1.8))
                page.keyboard.press("Enter")
                time.sleep(random.uniform(0.8, 1.8))
                
                if idx == 0 and image_path and image_path.exists():
                    print("Копирование обложки в буфер обмена для вставки...")
                    try:
                        with open(image_path, "rb") as img_file:
                            base64_data = base64.b64encode(img_file.read()).decode('utf-8')
                        
                        js_code = f"""
                        (async () => {{
                            try {{
                                const base64Data = "{base64_data}";
                                const byteCharacters = atob(base64Data);
                                const byteNumbers = new Array(byteCharacters.length);
                                for (let i = 0; i < byteCharacters.length; i++) {{
                                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                                }}
                                const byteArray = new Uint8Array(byteNumbers);
                                const blob = new Blob([byteArray], {{type: "image/png"}});
                                
                                await navigator.clipboard.write([
                                    new ClipboardItem({{
                                        [blob.type]: blob
                                    }})
                                ]);
                                return "OK";
                            }} catch (err) {{
                                return err.toString();
                            }}
                        }})()
                        """
                        res = page.evaluate(js_code)
                        print(f"Результат копирования картинки: {res}")
                        time.sleep(1.0)
                        
                        print("Вставляем обложку через Control+V...")
                        page.keyboard.press("Control+V")
                        time.sleep(7.0)
                        
                        page.keyboard.press("Enter")
                        time.sleep(random.uniform(1.0, 2.0))
                    except Exception as paste_err:
                        print(f"Не удалось вставить картинку: {paste_err}")

            print("Набор текста статьи успешно завершен!")
            time.sleep(random.uniform(3.0, 6.0))
            
            print("Поиск первой кнопки 'Опубликовать'...")
            publish_btn = page.get_by_text("Опубликовать").first
            publish_btn.wait_for(state="visible", timeout=15000)
            publish_btn.click()
            print("Нажата первая кнопка публикации...")
            time.sleep(random.uniform(4.0, 7.0))
            
            if "tags" in article_data and article_data["tags"]:
                print(f"Добавление тегов: {article_data['tags']}...")
                try:
                    tags_input = page.locator('input[placeholder*="Тег"], input[placeholder*="тег"], input[placeholder*="Тема"], input[placeholder*="тема"]').first
                    if tags_input.is_visible(timeout=5000):
                        tags_input.click()
                        time.sleep(0.5)
                        for tag in article_data["tags"]:
                            type_humanlike(page, tag)
                            time.sleep(random.uniform(0.3, 0.8))
                            page.keyboard.press("Enter")
                            time.sleep(random.uniform(0.5, 1.0))
                        print("Теги успешно добавлены.")
                except Exception as tag_err:
                    print(f"Не удалось добавить теги: {tag_err}")
            
            print("Нажатие финальной кнопки публикации...")
            final_publish_btn = page.locator('div[class*="settings"] button:has-text("Опубликовать"), button:has-text("Опубликовать сейчас"), button[type="submit"]:has-text("Опубликовать")').first
            
            if not final_publish_btn.is_visible():
                final_publish_btn = page.locator('button:has-text("Опубликовать"), div[class*="publish"] button').last
                
            final_publish_btn.wait_for(state="visible", timeout=15000)
            time.sleep(random.uniform(1.5, 3.0))
            final_publish_btn.click()
            print("Финальная кнопка публикации нажата!")
            
            time.sleep(10)
            print("Публикация успешно завершена!")
            
            screenshot_path = config.BASE_DIR / "latest_publication.png"
            page.screenshot(path=str(screenshot_path))
            print(f"Скриншот публикации сохранен в: {screenshot_path}")
            
            # Удаляем временный файл состояния при завершении
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

if __name__ == "__main__":
    test_article = {
        "title": "Тестовая статья " + str(time.time()),
        "content": "ВВЕДЕНИЕ В ИИ\nТестовое содержимое.\n\nВТОРОЙ РАЗДЕЛ\nДополнительный текст.",
        "tags": ["ии", "нейросети"]
    }
    publish_to_dzen(test_article, headless=True)
