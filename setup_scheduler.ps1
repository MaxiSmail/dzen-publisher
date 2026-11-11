# Multi-PC Windows Task Scheduler Setup for Neuro Autoposting
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$rootDir = $PSScriptRoot

# Динамический поиск папок без хардкода кириллицы
$progDir = Get-ChildItem -Path $rootDir -Directory | Where-Object { $_.Name -match "Программирование" }
$tgDir   = Get-ChildItem -Path $progDir.FullName -Directory | Where-Object { $_.Name -match "Автопостинг Telegram" }
$vkDir   = Get-ChildItem -Path $progDir.FullName -Directory | Where-Object { $_.Name -match "Автопостинг VK$" }
$dzenDir = Join-Path $rootDir ".agents\skills\dzen_publisher\scripts"

$tgBat   = Join-Path $tgDir.FullName "run.bat"
$vkBat   = Join-Path $vkDir.FullName "run.bat"
$dzenBat = Join-Path $dzenDir "run_dzen_agent.bat"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "НАСТРОЙКА РАСПИСАНИЯ АВТОПОСТИНГА (WINDOWS TASK SCHEDULER)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Путь Telegram: $tgBat"
Write-Host "Путь VK:       $vkBat"
Write-Host "Путь Dzen:     $dzenBat"

function Add-AutopostTask {
    param (
        [string]$TaskName,
        [string]$TimeStr,
        [string]$BatPath,
        [string]$Arguments = ""
    )

    Write-Host "`nРегистрация задачи: $TaskName на $TimeStr..." -ForegroundColor Yellow

    if (-not (Test-Path $BatPath)) {
        Write-Host "Ошибка: Файл не найден: $BatPath" -ForegroundColor Red
        return
    }

    $workingDir = Split-Path $BatPath -Parent

    if ($Arguments -ne "") {
        $action = New-ScheduledTaskAction -Execute $BatPath -Argument $Arguments -WorkingDirectory $workingDir
    } else {
        $action = New-ScheduledTaskAction -Execute $BatPath -WorkingDirectory $workingDir
    }

    $trigger = New-ScheduledTaskTrigger -Daily -At $TimeStr
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

    try {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
        Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Description "Автопостинг нейросетей ($TaskName)" | Out-Null
        Write-Host "✅ [УСПЕХ] Задача $TaskName зарегистрирована на $TimeStr ежедневно!" -ForegroundColor Green
    } catch {
        Write-Host "❌ [ОШИБКА] Не удалось зарегистрировать ${TaskName}: $_" -ForegroundColor Red
    }
}

# 1. VK Утро (09:00 МСК) - RSS пост
Add-AutopostTask -TaskName "Neuro_VK_Morning_0900" -TimeStr "09:00" -BatPath $vkBat -Arguments "own_rss"

# 2. Telegram Утро (09:05 МСК) - RSS пост
Add-AutopostTask -TaskName "Neuro_Telegram_Morning_0905" -TimeStr "09:05" -BatPath $tgBat

# 3. Яндекс.Дзен (13:00 МСК) - ИИ-Директор канала
Add-AutopostTask -TaskName "Neuro_Dzen_Director_1300" -TimeStr "13:00" -BatPath $dzenBat

# 4. VK День (13:50 МСК) - Адаптация статьи Дзена
Add-AutopostTask -TaskName "Neuro_VK_DzenAdapt_1350" -TimeStr "13:50" -BatPath $vkBat -Arguments "dzen_adaptation"

# 5. Telegram Вечер (18:00 МСК) - RSS пост
Add-AutopostTask -TaskName "Neuro_Telegram_Evening_1800" -TimeStr "18:00" -BatPath $tgBat

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "Все задачи успешно зарегистрированы в Windows Task Scheduler!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan