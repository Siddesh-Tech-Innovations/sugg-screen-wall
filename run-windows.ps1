# Suggestion Screen Wall - Windows PowerShell Setup and Launch Script
# This script sets up and runs the project on Windows using PowerShell

param(
    [switch]$SkipDependencyCheck
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Console colors and formatting
function Write-Header {
    param($Message)
    Write-Host "`n============================================" -ForegroundColor Cyan
    Write-Host "  $Message" -ForegroundColor Cyan
    Write-Host "============================================`n" -ForegroundColor Cyan
}

function Write-Success {
    param($Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error {
    param($Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Info {
    param($Message)
    Write-Host "📋 $Message" -ForegroundColor Yellow
}

# Get script directory
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ParentDir = Split-Path -Parent $ProjectDir

Write-Header "Suggestion Screen Wall - Windows Setup"

Write-Info "Project Directory: $ProjectDir"
Write-Info "Parent Directory: $ParentDir"

# Check if we're in the right directory
if (-not (Test-Path "$ProjectDir\frontend\package.json")) {
    Write-Error "frontend\package.json not found"
    Write-Error "Please run this script from the project root directory"
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path "$ProjectDir\simple-gcs-server.py")) {
    Write-Error "simple-gcs-server.py not found"
    Write-Error "Please run this script from the project root directory"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check for service account file
$ServiceAccountPath = "$ParentDir\suggestion-screen-service-account.json"
if (-not (Test-Path $ServiceAccountPath)) {
    Write-Error "Service account file not found"
    Write-Error "Please place 'suggestion-screen-service-account.json' in the parent directory"
    Write-Error "Expected location: $ServiceAccountPath"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Success "Service account file found"

if (-not $SkipDependencyCheck) {
    # Check if Python is installed
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -ne 0) { throw }
        Write-Success "Python found: $pythonVersion"
    }
    catch {
        Write-Error "Python is not installed or not in PATH"
        Write-Error "Please install Python 3.8+ from https://python.org"
        Read-Host "Press Enter to exit"
        exit 1
    }

    # Check if Node.js is installed
    try {
        $nodeVersion = node --version 2>&1
        if ($LASTEXITCODE -ne 0) { throw }
        Write-Success "Node.js found: $nodeVersion"
    }
    catch {
        Write-Error "Node.js is not installed or not in PATH"
        Write-Error "Please install Node.js from https://nodejs.org"
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Create Python virtual environment if it doesn't exist
$VenvPath = "$ProjectDir\.venv"
if (-not (Test-Path $VenvPath)) {
    Write-Info "Creating Python virtual environment..."
    try {
        python -m venv .venv
        Write-Success "Virtual environment created"
    }
    catch {
        Write-Error "Failed to create virtual environment"
        Read-Host "Press Enter to exit"
        exit 1
    }
}
else {
    Write-Success "Virtual environment already exists"
}

# Install Python dependencies
Write-Info "Installing Python dependencies..."
try {
    & "$VenvPath\Scripts\activate.ps1"
    pip install fastapi uvicorn google-cloud-storage requests
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Success "Python dependencies installed"
}
catch {
    Write-Error "Failed to install Python dependencies"
    Read-Host "Press Enter to exit"
    exit 1
}

# Install Node.js dependencies
Write-Info "Installing Node.js dependencies..."
try {
    Set-Location "$ProjectDir\frontend"
    npm install
    if ($LASTEXITCODE -ne 0) { throw }
    Set-Location $ProjectDir
    Write-Success "Node.js dependencies installed"
}
catch {
    Write-Error "Failed to install Node.js dependencies"
    Read-Host "Press Enter to exit"
    exit 1
}

# Setup cleanup
$BackendProcess = $null
$FrontendProcess = $null

function Stop-Servers {
    Write-Host "`n🛑 Shutting down servers..." -ForegroundColor Yellow
    
    if ($BackendProcess -and !$BackendProcess.HasExited) {
        $BackendProcess.Kill()
        Write-Host "✅ Backend server stopped" -ForegroundColor Green
    }
    
    if ($FrontendProcess -and !$FrontendProcess.HasExited) {
        $FrontendProcess.Kill()
        Write-Host "✅ Frontend server stopped" -ForegroundColor Green
    }
    
    # Kill any remaining processes
    Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*$ProjectDir*" } | Stop-Process -Force
    Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*node*" -and $_.CommandLine -like "*npm start*" } | Stop-Process -Force
    
    Write-Success "Cleanup complete"
}

# Register cleanup on exit
Register-EngineEvent PowerShell.Exiting -Action { Stop-Servers }

# Handle Ctrl+C
[Console]::CancelKeyPress += {
    Stop-Servers
    exit 0
}

Write-Header "Starting Suggestion Screen Wall"

Write-Host "🚀 Starting servers...`n" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend:  http://localhost:8001" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop both servers`n" -ForegroundColor Yellow

# Start backend server
Write-Host "=== STARTING BACKEND SERVER ===" -ForegroundColor Magenta
try {
    $BackendProcess = Start-Process -FilePath "$VenvPath\Scripts\python.exe" -ArgumentList "simple-gcs-server.py" -WorkingDirectory $ProjectDir -PassThru -WindowStyle Hidden
    Write-Success "Backend server started (PID: $($BackendProcess.Id))"
}
catch {
    Write-Error "Failed to start backend server"
    exit 1
}

# Wait for backend to start
Start-Sleep -Seconds 3

# Start frontend server
Write-Host "=== STARTING FRONTEND SERVER ===" -ForegroundColor Magenta
try {
    $FrontendProcess = Start-Process -FilePath "npm" -ArgumentList "start" -WorkingDirectory "$ProjectDir\frontend" -PassThru -WindowStyle Hidden
    Write-Success "Frontend server started (PID: $($FrontendProcess.Id))"
}
catch {
    Write-Error "Failed to start frontend server"
    Stop-Servers
    exit 1
}

Write-Host "`n✅ Both servers started successfully!`n" -ForegroundColor Green

Write-Host "🌐 Open your browser and go to: " -NoNewline -ForegroundColor Yellow
Write-Host "http://localhost:3000" -ForegroundColor Cyan

Write-Host "`n📱 The app will:" -ForegroundColor Yellow
Write-Host "  1. Capture your canvas drawing" -ForegroundColor White
Write-Host "  2. Upload to Google Cloud Storage" -ForegroundColor White
Write-Host "  3. Send via WhatsApp to configured recipients" -ForegroundColor White

# Keep script running
Write-Host "`nPress any key to stop the servers and exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Cleanup
Stop-Servers

Write-Host "`nThank you for using Suggestion Screen Wall!" -ForegroundColor Green
Read-Host "Press Enter to exit"