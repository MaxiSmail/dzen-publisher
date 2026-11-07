@echo off
cd /d "%~dp0"

echo [Dzen Agent] Запуск процесса генерации и автопубликации...

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe main.py
) else if exist "%USERPROFILE%\.gemini\config\skills\dzen_publisher\scripts\.venv\Scripts\python.exe" (
    "%USERPROFILE%\.gemini\config\skills\dzen_publisher\scripts\.venv\Scripts\python.exe" main.py
) else (
    where uv >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        uv run main.py
    ) else (
        python main.py
    )
)

if %ERRORLEVEL% equ 0 (
    echo [Dzen Agent] Публикация завершена успешно!
) else (
    echo [Dzen Agent] Произошла ошибка. Код выхода: %ERRORLEVEL%
)

timeout /t 5
