@echo off
chcp 65001 > nul
echo ============================================================
echo ЗАПУСК АВТОНОМНОГО VK-АВТОПОСТИНГА (ИИ + RSS)
echo ============================================================

if "%~1"=="" (
    echo Ошибка: не указан режим работы!
    echo Используйте: run.bat own_rss или run.bat dzen_adaptation
    pause
    exit /b 1
)

cd /d "%~dp0scripts"
"d:\Яндекс Диск\YandexDisk\выапорпоапраппаапр\Новая папка\Антигравити и Обсидиан\Antigravity\Проект ИИ-Директор Дзен Канала\scripts\.venv\Scripts\python.exe" main.py --mode %1
pause
