@echo off
cd /d "%~dp0"
echo [Dzen Agent] Запуск браузера для авторизации в Дзене...

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe login_helper.py
) else if exist "%USERPROFILE%\.gemini\config\skills\dzen_publisher\scripts\.venv\Scripts\python.exe" (
    "%USERPROFILE%\.gemini\config\skills\dzen_publisher\scripts\.venv\Scripts\python.exe" login_helper.py
) else (
    where uv >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        uv run login_helper.py
    ) else (
        python login_helper.py
    )
)
pause
