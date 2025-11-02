@echo off
setlocal enabledelayedexpansion

title Construction Estimation System

:: Check if Python is installed
echo.
echo ====================================================
echo 🏗️ CONSTRUCTION ESTIMATION SYSTEM
echo ====================================================
echo.

echo 🔍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo 📦 SOLUTIONS:
    echo    1. Download Python 3.8+ from https://python.org
    echo    2. During installation, check "Add Python to PATH"
    echo    3. Restart your computer after installation
    echo.
    echo ℹ️  After installing Python, double-click this file again
    echo.
    pause
    exit /b 1
)

echo ✅ Python is installed
echo.

:: Check if pip is available
echo 🔍 Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Pip not found, installing...
    python -m ensurepip --upgrade >nul 2>&1
)
echo ✅ Pip is ready
echo.

:: Install/update dependencies
echo 📦 Installing/updating required packages...
pip install -r requirements.txt > install_log.txt 2>&1
if %errorlevel% neq 0 (
    echo ❌ Failed to install packages
    echo.
    echo Check install_log.txt for details
    echo.
    echo 💡 Try these solutions:
    echo    1. Run Command Prompt as Administrator
    echo    2. Check your internet connection
    echo    3. Update pip: python -m pip install --upgrade pip
    echo.
    pause
    exit /b 1
)

echo ✅ All packages installed successfully
echo.

:: Launch the application
echo 🚀 Starting Construction Estimation System...
echo.
echo 📱 The app will open in your browser at http://localhost:8501
echo ⏹️  Press Ctrl+C in this window to stop the server
echo.
echo ====================================================
echo.

:: Run the Streamlit app
python -m streamlit run streamlit_estimation_app.py --server.address localhost --server.port 8501

:: Pause to show any error messages
if %errorlevel% neq 0 (
    echo.
    echo ❌ Application exited with error
    echo.
    pause
)
