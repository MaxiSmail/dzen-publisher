import requests
import json
import subprocess
import os

token = os.getenv("GITHUB_TOKEN")
repo_name = "obsidian-telegram-cloud"
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

if token and bot_token:
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 1. Создаем приватный репозиторий на GitHub
    print(f"[1/3] Создаем приватный репозиторий {repo_name} на GitHub...")
    url = "https://api.github.com/user/repos"
    data = {
        "name": repo_name,
        "description": "24/7 Cloud Telegram Bot for Obsidian (Private)",
        "private": True
    }
    resp = requests.post(url, headers=headers, json=data)

    if resp.status_code == 201:
        print("[Успех] Приватный репозиторий создан на GitHub!")
    elif resp.status_code == 422:
        print("[Информация] Репозиторий уже существует.")
    else:
        print(f"[Предупреждение] Ошибка создания репозитория ({resp.status_code}): {resp.text}")
