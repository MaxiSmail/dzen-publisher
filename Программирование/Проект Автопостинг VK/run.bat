@echo off
chcp 65001 > nul
echo ============================================================
echo ЗАПУСК АВТОНОМНОГО VK-АВТОПОСТИНГА (ИИ + RSS)
echo ============================================================

set MODE=%~1
if "%MODE%"=="" set MODE=own_rss

echo Режим запуска: %MODE%
cd /d "%~dp0scripts"

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe main.py --mode %MODE%
) else (
    where uv >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        uv run --with-requirements requirements.txt main.py --mode %MODE%
    ) else (
        python main.py --mode %MODE%
    )
)

if %ERRORLEVEL% equ 0 (
    echo [VK] Автопостинг успешно завершен!
) else (
    echo [VK] Ошибка выполнения. Код: %ERRORLEVEL%
)
