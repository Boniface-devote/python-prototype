@echo off
echo 🚀 PDF Data Extractor - Starting up...
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is not installed or not in PATH
    pause
    exit /b 1
)

echo ✅ Dependencies check passed
echo.

REM Install Python dependencies if needed
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

echo 📦 Activating virtual environment...
call venv\Scripts\activate.bat

echo 📦 Installing Python dependencies...
pip install -r requirements.txt

echo.
echo 🚀 Starting Flask backend...
start "Flask Backend" cmd /k "python app.py"

REM Wait for backend to start
timeout /t 5 /nobreak >nul

echo 🚀 Starting Next.js frontend...
cd frontend
start "Next.js Frontend" cmd /k "npm run dev"

echo.
echo 🎉 Application is starting!
echo 📱 Frontend will be available at: http://localhost:3000
echo 🔧 Backend will be available at: http://localhost:5000
echo.
echo Press any key to open the frontend in your browser...
pause >nul

start http://localhost:3000

echo.
echo ✅ Both services are running in separate windows
echo 👋 You can close this window now
pause
