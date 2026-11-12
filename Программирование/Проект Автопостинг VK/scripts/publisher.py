import requests
from pathlib import Path
import config
import os
import json

def create_vk_poll(question: str, options: list, group_id_int: int, token: str) -> str:
    """Создание интерактивного опроса ВКонтакте через polls.create API."""
    if not question or not options:
        return None
    try:
        url = "https://api.vk.com/method/polls.create"
        params = {
            "owner_id": -group_id_int,
            "question": question[:80],
            "add_answers": json.dumps(options[:5], ensure_ascii=False),
            "access_token": token,
            "v": "5.131"
        }
        res = requests.post(url, data=params, timeout=15)
        res.raise_for_status()
        data = res.json()
        if "response" in data:
            poll_info = data["response"]
            attachment_str = f"poll{poll_info['owner_id']}_{poll_info['id']}"
            print(f"Опрос успешно создан в ВК: {attachment_str}")
            return attachment_str
        elif "error" in data:
            print(f"⚠️ Ошибка создания опроса VK API: {data['error']['error_msg']}")
    except Exception as e:
        print(f"⚠️ Исключение при создании опроса в ВК: {e}")
    return None

def publish_to_vk(formatted_text: str, image_path: Path = None, poll_question: str = None, poll_options: list = None) -> bool:
    token = config.VK_ACCESS_TOKEN
    group_id = config.VK_GROUP_ID
    
    if not token or not group_id:
        print("Ошибка: VK_ACCESS_TOKEN или VK_GROUP_ID не заданы в .env!")
        return False
        
    try:
        group_id_int = abs(int(group_id))
    except Exception as e:
        print(f"Ошибка парсинга VK_GROUP_ID: {e}")
        return False
        
    print(f"Публикация поста во ВКонтакте в группу ID: {group_id_int}...")
    
    attachments = []
    
    # 1. Загрузка обложки
    if image_path and Path(image_path).exists():
        try:
            print("[1/3] Получение сервера загрузки фото...")
            upload_server_url = "https://api.vk.com/method/photos.getWallUploadServer"
            params = {
                "group_id": group_id_int,
                "access_token": token,
                "v": "5.131"
            }
            res = requests.get(upload_server_url, params=params, timeout=20)
            res.raise_for_status()
            server_data = res.json()
            
            if "response" in server_data:
                upload_url = server_data["response"]["upload_url"]
                
                print("[2/3] Отгрузка фото на сервер ВК...")
                with open(image_path, "rb") as f:
                    files = {"photo": f}
                    upload_res = requests.post(upload_url, files=files, timeout=30)
                upload_res.raise_for_status()
                upload_data = upload_res.json()
                
                print("[3/3] Сохранение фото в альбоме группы...")
                save_photo_url = "https://api.vk.com/method/photos.saveWallPhoto"
                save_params = {
                    "group_id": group_id_int,
                    "server": upload_data["server"],
                    "photo": upload_data["photo"],
                    "hash": upload_data["hash"],
                    "access_token": token,
                    "v": "5.131"
                }
                save_res = requests.post(save_photo_url, data=save_params, timeout=20)
                save_res.raise_for_status()
                save_data = save_res.json()
                
                if "response" in save_data and len(save_data["response"]) > 0:
                    photo_info = save_data["response"][0]
                    photo_attachment = f"photo{photo_info['owner_id']}_{photo_info['id']}"
                    attachments.append(photo_attachment)
                    print(f"Фото успешно прикреплено: {photo_attachment}")
        except Exception as img_err:
            print(f"⚠️ Не удалось загрузить картинку в ВК ({img_err}).")

    # 2. Создание интерактивного опроса
    if poll_question and poll_options:
        poll_attachment = create_vk_poll(poll_question, poll_options, group_id_int, token)
        if poll_attachment:
            attachments.append(poll_attachment)

    try:
        print("Создание записи на стене ВК...")
        post_url = "https://api.vk.com/method/wall.post"
        post_params = {
            "owner_id": -group_id_int,
            "from_group": 1,
            "message": formatted_text,
            "access_token": token,
            "v": "5.131"
        }
        if attachments:
            post_params["attachments"] = ",".join(attachments)
            
        post_res = requests.post(post_url, data=post_params, timeout=20)
        post_res.raise_for_status()
        post_data = post_res.json()
        
        # Обработка Flood control (код 9)
        if "error" in post_data and post_data["error"].get("error_code") == 9:
            import time
            print("⚠️ VK API Flood control. Ожидание 6 секунд перед повторной попыткой публикации...")
            time.sleep(6.0)
            post_res = requests.post(post_url, data=post_params, timeout=20)
            post_data = post_res.json()

        if "error" in post_data:
            print(f"Ошибка VK API (wall.post): {post_data['error']['error_msg']}")
            return False
            
        print(f"🎉 Пост успешно опубликован в ВК! ID записи: {post_data['response']['post_id']}")
        return True
        
    except Exception as e:
        print(f"Ошибка при публикации записи на стене ВК: {e}")
        return False

