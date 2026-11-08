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
    РЎРёРјСѓР»РёСЂСѓРµС‚ РµСЃС‚РµСЃС‚РІРµРЅРЅСѓСЋ РїРµС‡Р°С‚СЊ Р¶РёРІРѕРіРѕ С‡РµР»РѕРІРµРєР°:
    РІРІРѕРґРёС‚ СЃР»РѕРІР° СЃ РїР»Р°РІР°СЋС‰РёРјРё Р·Р°РґРµСЂР¶РєР°РјРё РєР»Р°РІРёС€ (10-35 РјСЃ) Рё РґРµР»Р°РµС‚ РїР°СѓР·С‹ РЅР° Р·РЅР°РєР°С… РїСЂРµРїРёРЅР°РЅРёСЏ.
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
    print("РќРђР§РђР›Рћ РџРЈР‘Р›РРљРђР¦РР Р’ Р”Р—Р•Рќ (РР-Р”РР Р•РљРўРћР  РљРђРќРђР›Рђ)")
    print("=" * 60)
    
    # РџРѕРґРґРµСЂР¶РєР° РіРёР±СЂРёРґРЅРѕРіРѕ СЂРµР¶РёРјР° Р°РІС‚РѕСЂРёР·Р°С†РёРё (Р›РѕРєР°Р»СЊРЅС‹Р№ РїСЂРѕС„РёР»СЊ РёР»Рё GitHub Secrets)
    session_secret_b64 = os.environ.get("DZEN_SESSION_STATE")
    storage_state_path = None
    
    if session_secret_b64:
        print("РћР±РЅР°СЂСѓР¶РµРЅ РѕР±Р»Р°С‡РЅС‹Р№ СЃРµРєСЂРµС‚ Р°РІС‚РѕСЂРёР·Р°С†РёРё DZEN_SESSION_STATE (GitHub Actions Mode)!")
        try:
            decoded_json = base64.b64decode(session_secret_b64.encode('utf-8')).decode('utf-8')
            storage_state_path = config.BASE_DIR / "temp_storage_state.json"
            with open(storage_state_path, "w", encoding="utf-8") as f:
                f.write(decoded_json)
        except Exception as err:
            print(f"РћС€РёР±РєР° РґРµРєРѕРґРёСЂРѕРІР°РЅРёСЏ DZEN_SESSION_STATE: {err}")

    if not storage_state_path and not config.USER_DATA_DIR.exists():
        print("РћС€РёР±РєР°: РїСЂРѕС„РёР»СЊ Р°РІС‚РѕСЂРёР·Р°С†РёРё РЅРµ РЅР°Р№РґРµРЅ!")
        print("Р—Р°РїСѓСЃС‚РёС‚Рµ login.bat РёР»Рё РґРѕР±Р°РІСЊС‚Рµ DZEN_SESSION_STATE РІ Secrets.")
        return False

    with sync_playwright() as p:
        print("Р—Р°РїСѓСЃРє Р±СЂР°СѓР·РµСЂР°...")
        if storage_state_path:
            # Р—Р°РїСѓСЃРє РІ РѕР±Р»Р°С‡РЅРѕРј СЂРµР¶РёРјРµ С‡РµСЂРµР· storage_state
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
            # Р›РѕРєР°Р»СЊРЅС‹Р№ Р·Р°РїСѓСЃРє С‡РµСЂРµР· persistent context
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(config.USER_DATA_DIR),
                headless=headless,
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled", "--start-maximized"],
                no_viewport=True,
                permissions=["clipboard-read", "clipboard-write"]
            )
        
        page = context.new_page()
        
        try:
            print("РџРµСЂРµС…РѕРґ РІ Р”Р·РµРЅ-СЃС‚СѓРґРёСЋ...")
            page.goto("https://dzen.ru/studio", wait_until="domcontentloaded", timeout=60000)
            time.sleep(random.uniform(4.0, 7.0))
            
            print("Р”Р·РµРЅ-СЃС‚СѓРґРёСЏ Р·Р°РіСЂСѓР¶РµРЅР°. РџСЂРѕРІРµСЂСЏРµРј СЃРµСЃСЃРёСЋ...")
            avatar_selector = '[class*="avatar"], [class*="profile"], header img, .header__avatar'
            avatar = page.locator(avatar_selector).first
            
            try:
                avatar.wait_for(state="visible", timeout=15000)
                print("РЎРµСЃСЃРёСЏ Р°РєС‚РёРІРЅР° (Р°РІР°С‚Р°СЂРєР° РїСЂРѕС„РёР»СЏ РЅР°Р№РґРµРЅР°).")
            except Exception:
                print("РћС€РёР±РєР°: Р°РІР°С‚Р°СЂРєР° РЅРµ РЅР°Р№РґРµРЅР°. РЎРµСЃСЃРёСЏ СѓСЃС‚Р°СЂРµР»Р°.")
                context.close()
                return False
                
            print("РљР»РёРєР°РµРј РїРѕ Р°РІР°С‚Р°СЂРєРµ РїСЂРѕС„РёР»СЏ...")
            avatar.click()
            time.sleep(random.uniform(1.5, 3.0))
            
            print("РљР»РёРєР°РµРј РїРѕ РєРЅРѕРїРєРµ 'РЎРѕР·РґР°С‚СЊ РїСѓР±Р»РёРєР°С†РёСЋ'...")
            create_pub_btn = page.get_by_text("РЎРѕР·РґР°С‚СЊ РїСѓР±Р»РёРєР°С†РёСЋ").first
            create_pub_btn.wait_for(state="visible", timeout=10000)
            create_pub_btn.click()
            time.sleep(random.uniform(1.5, 2.5))
            
            print("РљР»РёРєР°РµРј РїРѕ РїСѓРЅРєС‚Сѓ 'РќР°РїРёСЃР°С‚СЊ СЃС‚Р°С‚СЊСЋ'...")
            article_btn = page.get_by_text("РќР°РїРёСЃР°С‚СЊ СЃС‚Р°С‚СЊСЋ").first
            article_btn.wait_for(state="visible", timeout=10000)
            article_btn.click()
            print("Р’С‹Р±СЂР°РЅ РїСѓРЅРєС‚ 'РќР°РїРёСЃР°С‚СЊ СЃС‚Р°С‚СЊСЋ'. РћР¶РёРґР°РЅРёРµ Р·Р°РіСЂСѓР·РєРё СЂРµРґР°РєС‚РѕСЂР°...")
            time.sleep(random.uniform(5.0, 8.0))
            
            print("Р—Р°РєСЂС‹С‚РёРµ РїСЂРёРІРµС‚СЃС‚РІРµРЅРЅС‹С… РѕРєРѕРЅ...")
            page.keyboard.press("Escape")
            time.sleep(random.uniform(1.5, 2.5))
            
            print("Р’РІРѕРґ Р·Р°РіРѕР»РѕРІРєР° СЃС‚Р°С‚СЊРё...")
            title_element = page.locator('[contenteditable="true"]').first
            title_element.wait_for(state="visible", timeout=15000)
            title_element.click()
            time.sleep(random.uniform(0.5, 1.2))
            
            type_humanlike(page, article_data["title"])
            print(f"Р—Р°РіРѕР»РѕРІРѕРє СѓСЃРїРµС€РЅРѕ РЅР°Р±СЂР°РЅ: '{article_data['title']}'")
            time.sleep(random.uniform(1.5, 3.0))
            
            print("Р¤РѕРєСѓСЃРёСЂСѓРµРјСЃСЏ РЅР° С‚РµРєСЃС‚РѕРІРѕРј РїРѕР»Рµ...")
            body_element = page.locator('[contenteditable="true"]').nth(1)
            body_element.wait_for(state="visible", timeout=15000)
            body_element.focus()
            time.sleep(random.uniform(1.0, 2.0))
            
            paragraphs = [p.strip() for p in article_data["content"].split("\n") if p.strip()]
            print(f"Р’СЃРµРіРѕ Р°Р±Р·Р°С†РµРІ РґР»СЏ РЅР°Р±РѕСЂР°: {len(paragraphs)}")
            
            for idx, paragraph in enumerate(paragraphs):
                is_heading = paragraph.isupper() and len(paragraph) < 80 and not paragraph.endswith(".")
                
                if is_heading:
                    print(f"РџРµС‡Р°С‚СЊ РїРѕРґР·Р°РіРѕР»РѕРІРєР° H2: '{paragraph}'...")
                    page.keyboard.press("Control+B")
                    time.sleep(0.3)
                    type_humanlike(page, paragraph)
                    time.sleep(0.3)
                    page.keyboard.press("Control+B")
                else:
                    print(f"Р§РµР»РѕРІРµС‡РµСЃРєРёР№ РЅР°Р±РѕСЂ Р°Р±Р·Р°С†Р° {idx+1}/{len(paragraphs)}...")
                    type_humanlike(page, paragraph)
                
                time.sleep(random.uniform(0.8, 1.8))
                page.keyboard.press("Enter")
                time.sleep(random.uniform(0.8, 1.8))
                
                if idx == 0 and image_path and image_path.exists():
                    print("РљРѕРїРёСЂРѕРІР°РЅРёРµ РѕР±Р»РѕР¶РєРё РІ Р±СѓС„РµСЂ РѕР±РјРµРЅР° РґР»СЏ РІСЃС‚Р°РІРєРё...")
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
                        print(f"Р РµР·СѓР»СЊС‚Р°С‚ РєРѕРїРёСЂРѕРІР°РЅРёСЏ РєР°СЂС‚РёРЅРєРё: {res}")
                        time.sleep(1.0)
                        
                        print("Р’СЃС‚Р°РІР»СЏРµРј РѕР±Р»РѕР¶РєСѓ С‡РµСЂРµР· Control+V...")
                        page.keyboard.press("Control+V")
                        time.sleep(7.0)
                        
                        page.keyboard.press("Enter")
                        time.sleep(random.uniform(1.0, 2.0))
                    except Exception as paste_err:
                        print(f"РќРµ СѓРґР°Р»РѕСЃСЊ РІСЃС‚Р°РІРёС‚СЊ РєР°СЂС‚РёРЅРєСѓ: {paste_err}")

            print("РќР°Р±РѕСЂ С‚РµРєСЃС‚Р° СЃС‚Р°С‚СЊРё СѓСЃРїРµС€РЅРѕ Р·Р°РІРµСЂС€РµРЅ!")
            time.sleep(random.uniform(3.0, 6.0))
            
            print("РџРѕРёСЃРє РїРµСЂРІРѕР№ РєРЅРѕРїРєРё 'РћРїСѓР±Р»РёРєРѕРІР°С‚СЊ'...")
            publish_btn = page.get_by_text("РћРїСѓР±Р»РёРєРѕРІР°С‚СЊ").first
            publish_btn.wait_for(state="visible", timeout=15000)
            publish_btn.click()
            print("РќР°Р¶Р°С‚Р° РїРµСЂРІР°СЏ РєРЅРѕРїРєР° РїСѓР±Р»РёРєР°С†РёРё...")
            time.sleep(random.uniform(4.0, 7.0))
            
            if "tags" in article_data and article_data["tags"]:
                print(f"Р”РѕР±Р°РІР»РµРЅРёРµ С‚РµРіРѕРІ: {article_data['tags']}...")
                try:
                    tags_input = page.locator('input[placeholder*="РўРµРі"], input[placeholder*="С‚РµРі"], input[placeholder*="РўРµРјР°"], input[placeholder*="С‚РµРјР°"]').first
                    if tags_input.is_visible(timeout=5000):
                        tags_input.click()
                        time.sleep(0.5)
                        for tag in article_data["tags"]:
                            type_humanlike(page, tag)
                            time.sleep(random.uniform(0.3, 0.8))
                            page.keyboard.press("Enter")
                            time.sleep(random.uniform(0.5, 1.0))
                        print("РўРµРіРё СѓСЃРїРµС€РЅРѕ РґРѕР±Р°РІР»РµРЅС‹.")
                except Exception as tag_err:
                    print(f"РќРµ СѓРґР°Р»РѕСЃСЊ РґРѕР±Р°РІРёС‚СЊ С‚РµРіРё: {tag_err}")
            
            print("РќР°Р¶Р°С‚РёРµ С„РёРЅР°Р»СЊРЅРѕР№ РєРЅРѕРїРєРё РїСѓР±Р»РёРєР°С†РёРё...")
            final_publish_btn = page.locator('div[class*="settings"] button:has-text("РћРїСѓР±Р»РёРєРѕРІР°С‚СЊ"), button:has-text("РћРїСѓР±Р»РёРєРѕРІР°С‚СЊ СЃРµР№С‡Р°СЃ"), button[type="submit"]:has-text("РћРїСѓР±Р»РёРєРѕРІР°С‚СЊ")').first
            
            if not final_publish_btn.is_visible():
                final_publish_btn = page.locator('button:has-text("РћРїСѓР±Р»РёРєРѕРІР°С‚СЊ"), div[class*="publish"] button').last
                
            final_publish_btn.wait_for(state="visible", timeout=15000)
            time.sleep(random.uniform(1.5, 3.0))
            final_publish_btn.click()
            print("Р¤РёРЅР°Р»СЊРЅР°СЏ РєРЅРѕРїРєР° РїСѓР±Р»РёРєР°С†РёРё РЅР°Р¶Р°С‚Р°!")
            
            time.sleep(10)
            print("РџСѓР±Р»РёРєР°С†РёСЏ СѓСЃРїРµС€РЅРѕ Р·Р°РІРµСЂС€РµРЅР°!")
            
            screenshot_path = config.BASE_DIR / "latest_publication.png"
            page.screenshot(path=str(screenshot_path))
            print(f"РЎРєСЂРёРЅС€РѕС‚ РїСѓР±Р»РёРєР°С†РёРё СЃРѕС…СЂР°РЅРµРЅ РІ: {screenshot_path}")
            
            # РЈРґР°Р»СЏРµРј РІСЂРµРјРµРЅРЅС‹Р№ С„Р°Р№Р» СЃРѕСЃС‚РѕСЏРЅРёСЏ РїСЂРё Р·Р°РІРµСЂС€РµРЅРёРё
            if storage_state_path and storage_state_path.exists():
                try:
                    storage_state_path.unlink()
                except:
                    pass

            context.close()
            return True
            
        except TimeoutError as te:
            print(f"РџСЂРµРІС‹С€РµРЅРѕ РІСЂРµРјСЏ РѕР¶РёРґР°РЅРёСЏ СЌР»РµРјРµРЅС‚РѕРІ РёРЅС‚РµСЂС„РµР№СЃР°: {te}")
            err_screenshot = config.BASE_DIR / "error_screenshot.png"
            page.screenshot(path=str(err_screenshot))
            context.close()
            return False
        except Exception as e:
            print(f"РљСЂРёС‚РёС‡РµСЃРєР°СЏ РѕС€РёР±РєР° РїСЂРё РїСѓР±Р»РёРєР°С†РёРё: {e}")
            err_screenshot = config.BASE_DIR / "error_screenshot.png"
            try:
                page.screenshot(path=str(err_screenshot))
            except:
                pass
            context.close()
            return False

if __name__ == "__main__":
    test_article = {
        "title": "РўРµСЃС‚РѕРІР°СЏ СЃС‚Р°С‚СЊСЏ " + str(time.time()),
        "content": "Р’Р’Р•Р”Р•РќРР• Р’ РР\nРўРµСЃС‚РѕРІРѕРµ СЃРѕРґРµСЂР¶РёРјРѕРµ.\n\nР’РўРћР РћР™ Р РђР—Р”Р•Р›\nР”РѕРїРѕР»РЅРёС‚РµР»СЊРЅС‹Р№ С‚РµРєСЃС‚.",
        "tags": ["РёРё", "РЅРµР№СЂРѕСЃРµС‚Рё"]
    }
    publish_to_dzen(test_article, headless=True)
