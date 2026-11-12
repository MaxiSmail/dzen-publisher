# Multi-PC Windows Task Scheduler Setup for Neuro Autoposting
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$scriptDir = $PSScriptRoot
$pyScript = Join-Path $scriptDir "setup_scheduler.py"

if (-not (Test-Path $pyScript)) {
    Write-Host "Ошибка: Файл setup_scheduler.py не найден в $scriptDir" -ForegroundColor Red
    exit 1
}

Write-Host "Запуск кросс-платформенного конфигуратора Task Scheduler..." -ForegroundColor Cyan
python "$pyScript"
