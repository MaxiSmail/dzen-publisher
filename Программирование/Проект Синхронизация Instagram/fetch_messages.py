import sys
import os
import json
import re
import time
import hashlib
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

from config import (
    BROWSER_DATA_DIR,
    JSON_OUTPUT_FILE,
    MARKDOWN_OUTPUT_FILE,
    DEFAULT_CONFIG_FILE,
    OUTPUT_DIR
)

URL_REGEX = re.compile(r'https?://[^\s"\'<>]+')

def load_settings():
    settings = {
        "target_chat": "",
        "scroll_count": 5,
        "headless": False
    }
    if DEFAULT_CONFIG_FILE.exists():
        try:
            with open(DEFAULT_CONFIG_FILE, "r", encoding="utf-8") as f:
                settings.update(json.load(f))
        except Exception as e:
            print(f"[!] Ошибка чтения settings.json: {e}")
    return settings

def load_existing_materials():
    if JSON_OUTPUT_FILE.exists():
        try:
            with open(JSON_OUTPUT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_materials(materials):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(JSON_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(materials, f, ensure_ascii=False, indent=2)

    # Генерация Markdown файла
    generate_markdown(materials)

def categorize_url(url: str) -> str:
    url_lower = url.lower()
    if "instagram.com/reel/" in url_lower:
        return "Instagram Reel"
    elif "instagram.com/p/" in url_lower:
        return "Instagram Post"
    elif "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "YouTube Video"
    elif "github.com" in url_lower:
        return "GitHub Repo"
    elif "t.me" in url_lower:
        return "Telegram"
    else:
        return "External Link"

def generate_markdown(materials):
    lines = [
        "# 📚 База полезных материалов из Instagram",
        "",
        f"> Всего сохранено материалов: **{len(materials)}**",
        f"> Последнее обновление: **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**",
        "",
        "---",
        ""
    ]

    # Сортируем: самые свежие сверху
    sorted_items = sorted(materials, key=lambda x: x.get("first_seen", ""), reverse=True)

    for item in sorted_items:
        seen = item.get("first_seen", "Неизвестно")
        text = item.get("text", "").strip()
        urls = item.get("urls", [])

        lines.append(f"### 📌 Запись от {seen}")
        if text:
            # Цитата текста сообщения
            lines.append(f"> {text.replace(chr(10), ' ')}")
            lines.append("")

        if urls:
            lines.append("**Ссылки:**")
            for u in urls:
                cat = categorize_url(u)
                lines.append(f"- **[{cat}]** [{u}]({u})")
            lines.append("")

        lines.append("---")
        lines.append("")

    with open(MARKDOWN_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def extract_messages_from_page(page, scroll_count=5):
    print(f"[*] Сбор сообщений с прокруткой вверх ({scroll_count} раз)...")

    # Ищем контейнер с сообщениями (scrollable)
    # В Instagram web это обычно контейнер внутри основной области чата
    for i in range(scroll_count):
        try:
            # Пытаемся прокрутить колесиком или скриптом вверх
            page.mouse.wheel(0, -1200)
            time.sleep(1.2)
        except Exception:
            pass

    # Извлекаем все текстовые блоки и ссылки из области диалога
    extracted_data = page.evaluate("""() => {
        const results = [];
        // Находим все элементы-сообщения или строки
        // В IG это элементы с role="row" или блоки внутри диалога
        const messageRows = document.querySelectorAll('div[role="row"], div[dir="auto"]');

        // Также собираем все ссылки на странице
        const links = Array.from(document.querySelectorAll('a[href]')).map(a => a.href);

        // Находим блоки сообщений
        messageRows.forEach(row => {
            const text = (row.innerText || '').trim();
            const rowLinks = Array.from(row.querySelectorAll('a[href]')).map(a => a.href);
            if (text.length > 0 || rowLinks.length > 0) {
                results.push({
                    text: text,
                    links: rowLinks
                });
            }
        });

        return {
            messages: results,
            all_links: links
        };
    }""")

    return extracted_data

def sync_chat(target_chat=None):
    settings = load_settings()
    target = target_chat or settings.get("target_chat")
    scroll_count = settings.get("scroll_count", 5)
    is_headless = settings.get("headless", False)

    if not BROWSER_DATA_DIR.exists():
        print("[!] Папка профиля браузера не найдена!")
        print("Пожалуйста, сначала запустите авторизацию: python login.py")
        return

    print("=" * 60)
    print("=== СИНХРОНИЗАЦИЯ ДИАЛОГА INSTAGRAM ===")
    print("=" * 60)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_DATA_DIR),
            headless=is_headless,
            viewport={"width": 1280, "height": 800},
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )

        # Подгружаем куки из Яндекс.Браузера, если они были экспортированы
        cookies_file = OUTPUT_DIR / "instagram_cookies.json"
        if cookies_file.exists():
            try:
                with open(cookies_file, "r", encoding="utf-8") as f:
                    cookies = json.load(f)
                    context.add_cookies(cookies)
            except Exception:
                pass

        page = context.pages[0] if context.pages else context.new_page()

        # Если target передан как прямая ссылка
        if target and target.startswith("http"):
            print(f"[*] Переход по прямой ссылке на диалог: {target}")
            page.goto(target, wait_until="domcontentloaded")
        else:
            print("[*] Переход в Instagram Direct Inbox...")
            page.goto("https://www.instagram.com/direct/inbox/", wait_until="domcontentloaded")

            # Если задан никнейм друга
            if target:
                print(f"[*] Поиск диалога с '{target}'...")
                time.sleep(3)
                # Ищем элемент в списке чатов слева с текстом ника
                try:
                    chat_elem = page.locator(f"text={target}").first
                    if chat_elem.is_visible(timeout=5000):
                        print(f"[+] Найден диалог с {target}, открываем...")
                        chat_elem.click()
                    else:
                        print(f"[-] Диалог с {target} не найден в видимом списке. Откройте его вручную.")
                except Exception as e:
                    print(f"[-] Не удалось автоматически кликнуть на чат: {e}")

        # Ожидаем загрузки сообщений
        print("[*] Ожидание загрузки сообщений диалога...")
        time.sleep(4)

        current_url = page.url
        print(f"[*] Текущий URL: {current_url}")

        # Сохраняем URL в settings, если это прямая ссылка на тред
        if "/direct/t/" in current_url:
            settings["target_chat"] = current_url
            with open(DEFAULT_CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            print(f"[+] Сохранена прямая ссылка на чат: {current_url}")

        raw_data = extract_messages_from_page(page, scroll_count=scroll_count)
        context.close()

    # Обработка данных
    existing_items = load_existing_materials()
    existing_hashes = {item.get("id") for item in existing_items}
    existing_urls = set()
    for item in existing_items:
        for u in item.get("urls", []):
            existing_urls.add(u.strip())

    new_items = []
    messages = raw_data.get("messages", [])
    all_links = raw_data.get("all_links", [])

    # Ищем ссылки в сообщениях
    for msg in messages:
        text = msg.get("text", "")
        # Извлекаем ссылки из href и из текста
        links_in_row = msg.get("links", [])
        links_in_text = URL_REGEX.findall(text)
        all_msg_urls = list(dict.fromkeys(links_in_row + links_in_text))

        # Оставляем только содержательные ссылки (reels, posts, external)
        useful_urls = [
            u for u in all_msg_urls
            if "/direct/" not in u and "instagram.com/explore" not in u and not u.endswith("instagram.com/")
        ]

        if not text and not useful_urls:
            continue

        # Создаем уникальный идентификатор
        content_hash = hashlib.md5(f"{text}_{','.join(useful_urls)}".encode("utf-8")).hexdigest()

        if content_hash not in existing_hashes:
            # Проверяем, нет ли дубликатов по полезным ссылкам
            is_duplicate = False
            if useful_urls and all(u in existing_urls for u in useful_urls):
                is_duplicate = True

            if not is_duplicate:
                item = {
                    "id": content_hash,
                    "first_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "text": text,
                    "urls": useful_urls
                }
                new_items.append(item)
                existing_hashes.add(content_hash)
                for u in useful_urls:
                    existing_urls.add(u.strip())

    # Также проверим общие ссылки страницы на случай Reels
    for link in all_links:
        if ("/reel/" in link or "/p/" in link) and link not in existing_urls:
            content_hash = hashlib.md5(link.encode("utf-8")).hexdigest()
            if content_hash not in existing_hashes:
                item = {
                    "id": content_hash,
                    "first_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "text": "(Ссылка на публикацию/Reel)",
                    "urls": [link]
                }
                new_items.append(item)
                existing_hashes.add(content_hash)
                existing_urls.add(link)

    print(f"\n[+] Новых материалов найдено: {len(new_items)}")
    total_materials = existing_items + new_items
    save_materials(total_materials)

    print(f"[OK] Данные сохранены в:\n  -> {JSON_OUTPUT_FILE}\n  -> {MARKDOWN_OUTPUT_FILE}")

if __name__ == "__main__":
    target_arg = sys.argv[1] if len(sys.argv) > 1 else None
    sync_chat(target_arg)
