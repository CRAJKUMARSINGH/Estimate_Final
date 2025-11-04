@echo off
echo 🏗️ Starting Construction Estimation App...
echo ==========================================

echo Checking Python...
python --version

echo.
echo Installing required packages...
python -m pip install --user streamlit pandas numpy

echo.
echo Starting the app...
echo Open your browser to: http://localhost:8504
echo Press Ctrl+C to stop the app
echo.

python -m streamlit run ULTRA_SIMPLE_APP.py --server.port 8504

pause