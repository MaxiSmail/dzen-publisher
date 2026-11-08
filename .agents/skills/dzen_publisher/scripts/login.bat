@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo ============================================================
echo [Dzen Agent] Запуск браузера для авторизации в Дзене...
echo ============================================================

set "UV_EXE="
if exist "%LOCALAPPDATA%\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe" (
    set "UV_EXE=%LOCALAPPDATA%\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe"
) else if exist "%USERPROFILE%\.local\bin\uv.exe" (
    set "UV_EXE=%USERPROFILE%\.local\bin\uv.exe"
) else (
    where uv >nul 2>nul
    if %ERRORLEVEL% equ 0 set "UV_EXE=uv"
)

if defined UV_EXE (
    echo [OK] Запуск окружения через: "%UV_EXE%"
    "%UV_EXE%" run --with "playwright" --with "python-dotenv" --with "requests" --with "pynacl" python login_helper.py
) else (
    echo [Внимание] uv не найден, запуск через python...
    python login_helper.py
)

if %ERRORLEVEL% neq 0 (
    echo.
    echo ============================================================
    echo [ОШИБКА] Скрипт завершился с ошибкой (код %ERRORLEVEL%).
    echo Окно не закрывается, чтобы вы могли прочитать текст выше.
    echo ============================================================
)

echo.
echo Для закрытия окна нажмите любую клавишу...
pause > nul
