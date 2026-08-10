import requests
from pathlib import Path
import config
import os
import json

def publish_to_vk(formatted_text: str, image_path: Path = None) -> bool:
    token = config.VK_ACCESS_TOKEN
    group_id = config.VK_GROUP_ID # Идентификатор сообщества (число)
    
    if not token or not group_id:
        print("Ошибка: VK_ACCESS_TOKEN или VK_GROUP_ID не заданы в .env!")
        return False
        
    try:
        group_id_int = abs(int(group_id))
    except Exception as e:
        print(f"Ошибка парсинга VK_GROUP_ID: {e}")
        return False
        
    print(f"Публикация поста во ВКонтакте в группу ID: {group_id_int}...")
    
    attachment_str = None
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
                    attachment_str = f"photo{photo_info['owner_id']}_{photo_info['id']}"
                    print(f"Фото успешно загружено и прикреплено: {attachment_str}")
        except Exception as img_err:
            print(f"⚠️ Не удалось загрузить картинку в ВК ({img_err}), публикую только текст поста.")

    try:
        print("Создание записи на стене...")
        post_url = "https://api.vk.com/method/wall.post"
        post_params = {
            "owner_id": -group_id_int,
            "from_group": 1,
            "message": formatted_text,
            "access_token": token,
            "v": "5.131"
        }
        if attachment_str:
            post_params["attachments"] = attachment_str
            
        post_res = requests.post(post_url, data=post_params, timeout=20)
        post_res.raise_for_status()
        post_data = post_res.json()
        
        if "error" in post_data:
            print(f"Ошибка VK API (wall.post): {post_data['error']['error_msg']}")
            return False
            
        print(f"🎉 Пост успешно опубликован в ВК! ID записи: {post_data['response']['post_id']}")
        return True
        
    except Exception as e:
        print(f"Ошибка при публикации записи на стене ВК: {e}")
        return False
