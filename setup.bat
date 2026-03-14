@echo off
echo.
echo ======================================================================
echo STUDY TRACKER - COMPLETE SETUP GUIDE
echo ======================================================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] Node.js not installed!
    echo Please download from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo [✓] Node.js found: 
node -v
echo.

REM Install frontend dependencies
echo [*] Installing React frontend dependencies...
cd frontend
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [!] Failed to install npm packages
    pause
    exit /b 1
)
cd ..
echo [✓] Frontend dependencies installed
echo.

REM Show instructions
echo ======================================================================
echo SETUP COMPLETE! Follow these steps:
echo ======================================================================
echo.
echo STEP 1: Start MySQL Database
echo   - Open MySQL Command Line Client
echo   - Or ensure MySQL service is running
echo.
echo STEP 2: Start API Backend (Terminal/PowerShell 1)
echo   python api_server.py
echo.
echo STEP 3: Start React Frontend (Terminal/PowerShell 2)
echo   cd frontend
echo   npm start
echo.
echo The app will open at: http://localhost:3000
echo API runs on: http://localhost:5000/api
echo.
echo ======================================================================
echo.
pause
