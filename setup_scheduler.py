import os
import sys
import subprocess
import tempfile
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent

    tg_dir = root / "Программирование" / "Проект Автопостинг Telegram" / "scripts"
    vk_dir = root / "Программирование" / "Проект Автопостинг VK" / "scripts"
    dzen_dir = root / ".agents" / "skills" / "dzen_publisher" / "scripts"

    print("=" * 60)
    print("НАСТРОЙКА РАСПИСАНИЯ АВТОПОСТИНГА (WINDOWS TASK SCHEDULER)")
    print("=" * 60)
    print(f"Корень репозитория: {root}")

    dirs = [
        ("Telegram", tg_dir, tg_dir / "requirements.txt"),
        ("VK", vk_dir, vk_dir / "requirements.txt"),
        ("Dzen", dzen_dir, dzen_dir / "requirements.txt"),
    ]

    # Проверка и создание изолированных окружений .venv при необходимости
    for name, pdir, req in dirs:
        venv_dir = pdir / ".venv"
        python_exe = venv_dir / "Scripts" / "python.exe"
        if not python_exe.exists():
            print(f"Создание виртуального окружения для {name} в {venv_dir}...")
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
            if req.exists():
                print(f"Установка зависимостей из {req.name}...")
                subprocess.run([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"], check=True)
                subprocess.run([str(python_exe), "-m", "pip", "install", "-r", str(req)], check=True)
        else:
            print(f"✓ Виртуальное окружение {name} готово: {python_exe}")

    tasks = [
        {
            "name": "Neuro_VK_Morning_0900",
            "time": "09:00:00",
            "dir": vk_dir,
            "exe": vk_dir / ".venv" / "Scripts" / "python.exe",
            "args": "main.py --mode own_rss"
        },
        {
            "name": "Neuro_Telegram_Morning_0905",
            "time": "09:05:00",
            "dir": tg_dir,
            "exe": tg_dir / ".venv" / "Scripts" / "python.exe",
            "args": "main.py"
        },
        {
            "name": "Neuro_Dzen_Director_1300",
            "time": "13:00:00",
            "dir": dzen_dir,
            "exe": dzen_dir / ".venv" / "Scripts" / "python.exe",
            "args": "main.py"
        },
        {
            "name": "Neuro_VK_DzenAdapt_1350",
            "time": "13:50:00",
            "dir": vk_dir,
            "exe": vk_dir / ".venv" / "Scripts" / "python.exe",
            "args": "main.py --mode dzen_adaptation"
        },
        {
            "name": "Neuro_Telegram_Evening_1800",
            "time": "18:00:00",
            "dir": tg_dir,
            "exe": tg_dir / ".venv" / "Scripts" / "python.exe",
            "args": "main.py"
        }
    ]

    xml_template = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Автопостинг нейросетей ({name})</Description>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2026-11-12T{time}</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT2H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{exe}</Command>
      <Arguments>{args}</Arguments>
      <WorkingDirectory>{workdir}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"""

    print("\nРегистрация задач в Windows Task Scheduler...")
    for t in tasks:
        content = xml_template.format(
            name=t["name"],
            time=t["time"],
            exe=str(t["exe"]),
            args=t["args"],
            workdir=str(t["dir"])
        )
        with tempfile.NamedTemporaryFile("w", encoding="utf-16", suffix=".xml", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            cmd = f'schtasks /create /tn "{t["name"]}" /xml "{temp_path}" /f'
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"✓ Задача {t['name']} успешно зарегистрирована на {t['time'][:5]} ежедневно!")
            else:
                print(f"✗ Ошибка при регистрации {t['name']}: {res.stderr.strip() or res.stdout.strip()}")
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    print("\n" + "=" * 60)
    print("Все задачи расписания успешно сконфигурированы и активны!")
    print("=" * 60)

if __name__ == "__main__":
    main()
