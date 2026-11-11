@echo off
chcp 65001 > nul
echo ============================================================
echo ЗАПУСК АВТОНОМНОГО TELEGRAM-АВТОПОСТИНГА
echo ============================================================
cd /d "%~dp0scripts"

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe main.py
) else (
    where uv >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        uv run --with-requirements requirements.txt main.py
    ) else (
        python main.py
    )
)

if %ERRORLEVEL% equ 0 (
    echo [Telegram] Цикл автопостинга успешно завершен!
) else (
    echo [Telegram] Ошибка выполнения. Код: %ERRORLEVEL%
)
