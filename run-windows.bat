@echo off
setlocal enabledelayedexpansion

REM Suggestion Screen Wall - Windows Setup and Launch Script
REM This script sets up and runs the project on Windows

echo.
echo ============================================
echo   Suggestion Screen Wall - Windows Setup
echo ============================================
echo.

REM Get the current directory (project root)
set PROJECT_DIR=%~dp0
set PARENT_DIR=%PROJECT_DIR%..

echo Project Directory: %PROJECT_DIR%
echo Parent Directory: %PARENT_DIR%

REM Check if we're in the right directory
if not exist "%PROJECT_DIR%frontend\package.json" (
    echo ERROR: frontend\package.json not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

if not exist "%PROJECT_DIR%simple-gcs-server.py" (
    echo ERROR: simple-gcs-server.py not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check for service account file
if not exist "%PARENT_DIR%\suggestion-screen-service-account.json" (
    echo ERROR: Service account file not found
    echo Please place 'suggestion-screen-service-account.json' in the parent directory
    echo Expected location: %PARENT_DIR%\suggestion-screen-service-account.json
    pause
    exit /b 1
)

echo ✅ Service account file found
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo ✅ Node.js found
node --version
echo.

REM Create Python virtual environment if it doesn't exist
if not exist "%PROJECT_DIR%.venv\" (
    echo 📦 Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Install Python dependencies
echo.
echo 📦 Installing Python dependencies...
call .venv\Scripts\activate.bat
pip install fastapi uvicorn google-cloud-storage requests
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo ✅ Python dependencies installed

REM Install Node.js dependencies
echo.
echo 📦 Installing Node.js dependencies...
cd frontend
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install Node.js dependencies
    pause
    exit /b 1
)
cd ..
echo ✅ Node.js dependencies installed

REM Create a cleanup function
set "cleanup_done=false"

REM Function to cleanup processes
:cleanup
if "!cleanup_done!"=="true" goto :eof
set "cleanup_done=true"
echo.
echo 🛑 Shutting down servers...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1
echo ✅ Cleanup complete
goto :eof

REM Set up Ctrl+C handler
if not defined CLEANUP_HANDLER (
    set CLEANUP_HANDLER=1
    call :cleanup >nul 2>&1
)

echo.
echo ============================================
echo   Starting Suggestion Screen Wall
echo ============================================
echo.
echo 🚀 Starting servers...
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8001
echo.
echo Press Ctrl+C to stop both servers
echo.

REM Start Python backend server
echo === STARTING BACKEND SERVER ===
start "Backend Server" cmd /c "cd /d "%PROJECT_DIR%" && .venv\Scripts\activate.bat && python simple-gcs-server.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start React frontend
echo === STARTING FRONTEND SERVER ===
cd frontend
start "Frontend Server" cmd /c "npm start"
cd ..

echo.
echo ✅ Both servers started successfully!
echo.
echo 🌐 Open your browser and go to: http://localhost:3000
echo.
echo 📱 The app will:
echo   1. Capture your canvas drawing
echo   2. Upload to Google Cloud Storage
echo   3. Send via WhatsApp to configured recipients
echo.

REM Keep the script running and wait for user to press a key
echo Press any key to stop the servers and exit...
pause >nul

REM Cleanup when script exits
call :cleanup

echo.
echo Thank you for using Suggestion Screen Wall!
pause