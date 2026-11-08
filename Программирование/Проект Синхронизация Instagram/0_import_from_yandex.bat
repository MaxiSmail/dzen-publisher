@echo off
chcp 65001 > nul
echo Запуск импорта авторизации из Яндекс.Браузера...
python "%~dp0import_yandex_session.py"
pause
