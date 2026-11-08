import os
import sys
import json
import base64
import sqlite3
import shutil
import time
import subprocess
from pathlib import Path
import win32crypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from playwright.sync_api import sync_playwright

from config import BROWSER_DATA_DIR, OUTPUT_DIR

COOKIES_JSON = OUTPUT_DIR / "instagram_cookies.json"

def is_yandex_running():
    cmd = 'tasklist /FI "IMAGENAME eq browser.exe" /NH'
    output = subprocess.check_output(cmd, shell=True).decode("cp866", errors="ignore")
    return "browser.exe" in output.lower()

def close_yandex_background():
    print("[*] Закрытие фоновых процессов Яндекс.Браузера...")
    os.system("taskkill /F /IM browser.exe >nul 2>&1")
    time.sleep(1)

def restart_yandex():
    yandex_path = r"C:\Program Files\Yandex\YandexBrowser\Application\browser.exe"
    if os.path.exists(yandex_path):
        print("[*] Перезапуск Яндекс.Браузера...")
        subprocess.Popen([yandex_path])

def get_yandex_aes_key():
    local_state_path = Path(os.path.expandvars(r'%LOCALAPPDATA%\Yandex\YandexBrowser\User Data\Local State'))
    if not local_state_path.exists():
        raise FileNotFoundError(f"Файл Local State не найден: {local_state_path}")
    
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)

    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    aes_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return aes_key

def chromium_to_unix_time(expires_utc):
    if expires_utc == 0:
        return -1
    return int((expires_utc / 1000000) - 11644473600)

def extract_instagram_cookies(aes_key):
    src_cookies = Path(os.path.expandvars(r'%LOCALAPPDATA%\Yandex\YandexBrowser\User Data\Default\Network\Cookies'))
    if not src_cookies.exists():
        raise FileNotFoundError(f"Файл Cookies не найден: {src_cookies}")

    tmp_cookies = Path(os.path.expandvars(r'%TEMP%\yandex_cookies_ig.db'))
    
    # Если браузер всё ещё держит блокировку, закрываем фоновые процессы
    if is_yandex_running():
        close_yandex_background()

    copied = False
    for _ in range(5):
        try:
            shutil.copy2(src_cookies, tmp_cookies)
            copied = True
            break
        except Exception:
            time.sleep(0.5)

    if not copied:
        raise PermissionError("Не удалось получить доступ к файлу кук Яндекс.Браузера.")

    conn = sqlite3.connect(tmp_cookies)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT host_key, name, path, encrypted_value, expires_utc, is_secure, is_httponly, samesite
        FROM cookies
        WHERE host_key LIKE '%instagram%'
    """)
    rows = cursor.fetchall()
    conn.close()

    if tmp_cookies.exists():
        try:
            tmp_cookies.unlink()
        except Exception:
            pass

    aesgcm = AESGCM(aes_key)
    playwright_cookies = []

    samesite_map = {
        0: "None",
        1: "Lax",
        2: "Strict"
    }

    for host_key, name, path, enc_val, expires_utc, is_secure, is_httponly, samesite in rows:
        try:
            if enc_val.startswith(b"v10") or enc_val.startswith(b"v11"):
                iv = enc_val[3:15]
                ciphertext = enc_val[15:]
                raw = aesgcm.decrypt(iv, ciphertext, None)
            else:
                raw = win32crypt.CryptUnprotectData(enc_val, None, None, None, 0)[1]

            # В современных версиях Chromium может быть 32-байтный заголовок
            try:
                value = raw.decode("utf-8")
            except Exception:
                value = raw[32:].decode("utf-8", errors="ignore")

            # Чистим domain от ведущей точки для соответствия Playwright или оставляем как есть
            clean_domain = host_key if host_key.startswith(".") else ("." + host_key)

            cookie_dict = {
                "name": name,
                "value": value,
                "domain": clean_domain,
                "path": path or "/",
                "httpOnly": bool(is_httponly),
                "secure": bool(is_secure),
                "sameSite": samesite_map.get(samesite, "Lax")
            }
            exp = chromium_to_unix_time(expires_utc)
            if exp > 0:
                cookie_dict["expires"] = exp

            playwright_cookies.append(cookie_dict)
        except Exception as e:
            continue

    return playwright_cookies

def import_session(auto_restart=True):
    print("=" * 60)
    print("=== ИМПОРТ АВТОРИЗАЦИИ ИЗ ЯНДЕКС.БРАУЗЕРА ===")
    print("=" * 60)

    try:
        aes_key = get_yandex_aes_key()
        cookies = extract_instagram_cookies(aes_key)
        
        has_session = any(c["name"] == "sessionid" for c in cookies)
        if not has_session:
            print("[!] Внимание: куки Instagram найдены, но кука 'sessionid' отсутствует.")
            print("Убедитесь, что в Яндекс.Браузере вы действительно залогинены на https://www.instagram.com")
            if auto_restart:
                restart_yandex()
            return False

        print(f"[+] Успешно извлечено кук Instagram: {len(cookies)}")
        
        # Сохраняем в JSON
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(COOKIES_JSON, "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)

        # Теперь внедряем их в профиль Playwright
        print("[*] Внедрение кук в браузерный профиль Playwright...")
        BROWSER_DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(BROWSER_DATA_DIR),
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            context.add_cookies(cookies)
            
            # Проверяем работу кук
            page = context.new_page()
            print("[*] Проверка входа в Instagram Direct...")
            page.goto("https://www.instagram.com/direct/inbox/", wait_until="domcontentloaded")
            time.sleep(3)
            
            final_url = page.url
            print(f"[*] Итоговый URL проверки: {final_url}")
            
            if "login" in final_url.lower():
                print("[-] Сессия не принята (редирект на страницу входа).")
                context.close()
                if auto_restart:
                    restart_yandex()
                return False
            else:
                print("\n" + "=" * 60)
                print("[УСПЕХ!] Авторизация успешно скопирована!")
                print(f"Пользователь с ID {next((c['value'] for c in cookies if c['name'] == 'ds_user_id'), '')} авторизован.")
                print("=" * 60)
                context.close()
                if auto_restart:
                    restart_yandex()
                return True

    except Exception as e:
        print(f"\n[Ошибка] Не удалось скопировать сессию: {e}")
        if auto_restart:
            restart_yandex()
        return False

if __name__ == "__main__":
    import_session()
