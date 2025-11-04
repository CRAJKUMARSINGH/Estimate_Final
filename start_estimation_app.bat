@echo off
echo 🏗️ Starting Construction Estimation App...
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python.
    pause
    exit /b
)

echo.
echo Installing required packages...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ⚠️ Warning: Could not install packages. Continuing anyway...
)

echo.
echo 🚀 Launching Construction Estimation App...
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the app
echo.

python -m streamlit run app.py --server.port 8501

echo.
echo 👋 App stopped.