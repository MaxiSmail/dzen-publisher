@echo off
chcp 65001 > nul
echo Запуск синхронизации диалога...
python "%~dp0fetch_messages.py" %*
pause
