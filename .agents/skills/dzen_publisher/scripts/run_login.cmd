@echo off
cd /d "%~dp0"
echo ============================================================
echo Starting Dzen Login Helper...
echo ============================================================

"C:\Users\maksi\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe" run --with playwright --with python-dotenv python login_helper.py

pause
