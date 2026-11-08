$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Запуск помощника авторизации Дзен..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$uv = "C:\Users\maksi\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe"
if (-not (Test-Path $uv)) {
    $uv = (Get-Command uv -ErrorAction SilentlyContinue).Source
}

& $uv run --with playwright --with python-dotenv python login_helper.py
