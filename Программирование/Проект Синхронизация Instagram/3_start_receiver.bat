@echo off
chcp 65001 > nul
echo Запуск локального приёмника материалов Антигравити...
python "%~dp0server.py"
pause
