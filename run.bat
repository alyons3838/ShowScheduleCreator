@echo off
REM Quick start script for Windows

echo ==========================================
echo Thousand Hills Vacations
echo Show Schedule Creator
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Run the application
echo.
echo Starting application...
echo Open your browser to: http://127.0.0.1:5000
echo Press Ctrl+C to stop
echo.
python app.py

pause
