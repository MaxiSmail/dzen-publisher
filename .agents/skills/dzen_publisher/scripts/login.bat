@echo off
cd /d "%~dp0"
echo [Dzen Agent] Запуск браузера для авторизации в Дзене...
.venv\Scripts\python.exe login_helper.py
pause
