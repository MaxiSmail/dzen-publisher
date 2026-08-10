@echo off
cd /d "%~dp0"
echo [Dzen Agent] Запуск автоматической генерации и публикации статьи...
.venv\Scripts\python.exe main.py
pause
