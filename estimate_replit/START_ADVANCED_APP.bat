@echo off
cls
echo.
echo 🏗️ ADVANCED CONSTRUCTION ESTIMATION SYSTEM
echo ============================================
echo.
echo 🚀 Starting your most advanced construction estimation app...
echo 📊 This includes ALL the features you've been working on:
echo.
echo    ✅ Enhanced Excel Import with Formula Preservation
echo    ✅ Real-time Calculations and Updates  
echo    ✅ Database Persistence and Project Management
echo    ✅ Advanced Search and Filtering
echo    ✅ Visual Analytics and Reporting
echo    ✅ Template System for Reusable Estimates
echo    ✅ Multi-user Collaboration Support
echo    ✅ Professional UI/UX Design
echo.
echo 🌐 The app will open at: http://localhost:8509
echo ⏹️  Press Ctrl+C to stop the app
echo.
echo Starting in 3 seconds...
timeout /t 3 /nobreak >nul

echo 📦 Installing/checking required packages...
python -m pip install --user streamlit pandas numpy plotly openpyxl sqlite3 >nul 2>&1

echo 🚀 Launching advanced app...
echo.

REM Try the most advanced version first
if exist construction_estimation_app.py (
    echo 🎯 Running: construction_estimation_app.py (Most Advanced Version)
    python -m streamlit run construction_estimation_app.py --server.port 8509
) else if exist streamlit_app.py (
    echo 🎯 Running: streamlit_app.py (Comprehensive Version)  
    python -m streamlit run streamlit_app.py --server.port 8509
) else if exist SIMPLE_APP.py (
    echo 🎯 Running: SIMPLE_APP.py (Simplified Version)
    python -m streamlit run SIMPLE_APP.py --server.port 8509
) else (
    echo ❌ No app file found!
    echo Available Python files:
    dir *.py /b
)

echo.
echo 👋 App stopped. Press any key to exit...
pause >nul