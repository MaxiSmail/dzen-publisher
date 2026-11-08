@echo off
chcp 65001 > nul
echo Запуск авторизации в Instagram...
python "%~dp0login.py"
pause
