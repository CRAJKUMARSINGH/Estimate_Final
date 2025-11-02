@echo off
title Construction Estimation System

echo ====================================================
echo 🏗️ CONSTRUCTION ESTIMATION SYSTEM - QUICK START
echo ====================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found!
    echo.
    echo Please install Python and double-click 'run_app.bat' instead
    echo.
    pause
    exit /b 1
)

:: Quick check for streamlit
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Streamlit not installed
    echo.
    echo Running full setup - please wait...
    echo.
    call run_app.bat
    exit /b 0
)

:: Launch the application directly
echo 🚀 Starting Construction Estimation System...
echo.
echo 📱 Opening browser at http://localhost:8501
echo ⏹️  Press Ctrl+C to stop the server
echo.
echo ====================================================
echo.

:: Run the Streamlit app
python -m streamlit run streamlit_estimation_app.py --server.address localhost --server.port 8501

:: Pause to show any error messages
if %errorlevel% neq 0 (
    echo.
    echo ❌ Application error occurred
    echo.
    pause
)