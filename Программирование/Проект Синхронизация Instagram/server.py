import http.server
import socketserver
import json
from datetime import datetime
from pathlib import Path
from fetch_messages import save_materials, load_existing_materials, URL_REGEX
from config import JSON_OUTPUT_FILE, MARKDOWN_OUTPUT_FILE, OUTPUT_DIR

PORT = 54321

class InstagramReceiverHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS, GET")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        self._set_headers(200)
        self.wfile.write(json.dumps({"status": "running", "service": "Antigravity Instagram Sync"}).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            payload = json.loads(post_data.decode("utf-8"))
            items = payload.get("items", [])
            print(f"[*] Получено элементов из браузера: {len(items)}")

            existing_items = load_existing_materials()
            existing_hashes = {item.get("id") for item in existing_items}
            existing_urls = set()
            for it in existing_items:
                for u in it.get("urls", []):
                    existing_urls.add(u.strip())

            new_count = 0
            for it in items:
                text = it.get("text", "").strip()
                urls = it.get("urls", [])
                
                # Поиск ссылок в тексте дополнительно
                if text:
                    found_urls = URL_REGEX.findall(text)
                    urls = list(dict.fromkeys(urls + found_urls))

                # Убираем системные ссылки
                clean_urls = [
                    u for u in urls
                    if "/direct/" not in u and not u.endswith("instagram.com/") and "instagram.com/explore" not in u
                ]

                if not text and not clean_urls:
                    continue

                import hashlib
                item_hash = hashlib.md5(f"{text}_{','.join(clean_urls)}".encode("utf-8")).hexdigest()

                if item_hash not in existing_hashes:
                    # Проверяем дубликаты ссылок
                    if clean_urls and all(u in existing_urls for u in clean_urls):
                        continue

                    entry = {
                        "id": item_hash,
                        "first_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "text": text,
                        "urls": clean_urls
                    }
                    existing_items.append(entry)
                    existing_hashes.add(item_hash)
                    for u in clean_urls:
                        existing_urls.add(u.strip())
                    new_count += 1

            save_materials(existing_items)
            print(f"[+] Успешно сохранено новых записей: {new_count}. Всего: {len(existing_items)}")

            self._set_headers(200)
            response = {
                "success": True,
                "new_items": new_count,
                "total_items": len(existing_items),
                "message": f"Добавлено {new_count} новых материалов!"
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))

        except Exception as e:
            print(f"[!] Ошибка обработки данных: {e}")
            self._set_headers(500)
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def log_message(self, format, *args):
        # Отключаем лишний шум в консоли
        return

def run_server():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    server_address = ("127.0.0.1", PORT)
    with socketserver.TCPServer(server_address, InstagramReceiverHandler) as httpd:
        print("=" * 60)
        print(f"=== ПРИЁМНИК МАТЕРИАЛОВ INSTAGRAM ЗАПУЩЕН НА ПОРТУ {PORT} ===")
        print("=" * 60)
        print("Теперь, когда вы открыли диалог в Яндекс.Браузере,")
        print("просто нажмите кнопку/закладку 'Синхронизировать с Антигравити'.")
        print(f"Файлы сохраняются в:\n  -> {MARKDOWN_OUTPUT_FILE}\n  -> {JSON_OUTPUT_FILE}")
        print("\nОжидание данных... (для остановки закройте это окно)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nОстановка сервера...")

if __name__ == "__main__":
    run_server()
