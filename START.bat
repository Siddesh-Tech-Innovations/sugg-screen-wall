@echo off
REM Suggestion Screen Wall - Universal Windows Launcher
REM This script automatically chooses the best method to run the application

echo.
echo ============================================
echo    Suggestion Screen Wall - Launcher
echo ============================================
echo.

REM Check if PowerShell is available and execution policy allows scripts
powershell -Command "Get-ExecutionPolicy" >nul 2>&1
if %errorlevel% == 0 (
    echo 🚀 Launching with PowerShell script...
    powershell -ExecutionPolicy Bypass -File "%~dp0run-windows.ps1"
) else (
    echo 🚀 Launching with Batch script...
    call "%~dp0run-windows.bat"
)

echo.
pause