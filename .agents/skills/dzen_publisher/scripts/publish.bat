@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo [Dzen Agent] Запуск автоматической генерации и публикации статьи...

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe main.py %*
) else (
    where uv >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        uv run --with-requirements requirements.txt main.py %*
    ) else (
        python main.py %*
    )
)

if %ERRORLEVEL% equ 0 (
    echo [Dzen Agent] Публикация завершена успешно!
) else (
    echo [Dzen Agent] Ошибка публикации. Код выхода: %ERRORLEVEL%
)
