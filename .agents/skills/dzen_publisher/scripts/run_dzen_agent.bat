@echo off
:: Переходим в папку, где лежит этот скрипт
cd /d "%~dp0"

echo [Dzen Agent] Запуск процесса генерации и автопубликации...

:: Запускаем скрипт через интерпретатор Python виртуального окружения
.venv\Scripts\python.exe main.py

if %ERRORLEVEL% equ 0 (
    echo [Dzen Agent] Публикация завершена успешно!
) else (
    echo [Dzen Agent] Произошла ошибка. Код выхода: %ERRORLEVEL%
)

:: Задержка 5 секунд перед закрытием окна при ручном запуске
timeout /t 5
