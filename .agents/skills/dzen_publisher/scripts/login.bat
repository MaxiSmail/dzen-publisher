@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0login.ps1"
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Process exited with error code %ERRORLEVEL%
)
pause
