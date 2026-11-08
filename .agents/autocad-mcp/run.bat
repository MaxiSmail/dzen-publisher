@echo off
setlocal
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
where uv >nul 2>nul
if %ERRORLEVEL% equ 0 (
    uv run --with pywin32 --with "mcp<2" python "%~dp0server.py" %*
) else (
    "%USERPROFILE%\.local\bin\uv.exe" run --with pywin32 --with "mcp<2" python "%~dp0server.py" %*
)
