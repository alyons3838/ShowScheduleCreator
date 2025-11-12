@echo off
REM Build script for creating Windows executable

echo ==========================================
echo Building Thousand Hills Schedule Creator
echo Windows Executable
echo ==========================================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found.
    echo Please run: python -m venv venv
    echo Then: venv\Scripts\activate.bat
    echo Then: pip install -r requirements.txt
    exit /b 1
)

REM Ensure PyInstaller is installed
echo Checking dependencies...
pip install -q pyinstaller

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec

REM Build the application
echo Building executable...
echo This may take a few minutes...
echo.

pyinstaller --noconfirm ^
    --name="ThousandHillsScheduleCreator" ^
    --onefile ^
    --windowed ^
    --icon=NONE ^
    --add-data="templates;templates" ^
    --add-data="static;static" ^
    --hidden-import="pdfplumber" ^
    --hidden-import="reportlab" ^
    --hidden-import="PIL" ^
    --hidden-import="werkzeug" ^
    --collect-all="reportlab" ^
    --collect-all="pdfplumber" ^
    launcher.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==========================================
    echo Build successful!
    echo ==========================================
    echo.
    echo Your application is ready at:
    echo   dist\ThousandHillsScheduleCreator.exe
    echo.
    echo To distribute to your reps:
    echo 1. Copy the .exe file to a USB drive or
    echo 2. Zip it and send via email/cloud storage
    echo.
    echo Users just need to:
    echo 1. Copy the .exe anywhere on their computer
    echo 2. Double-click to run
    echo.
    echo Windows may show a security warning on first run.
    echo Click "More info" then "Run anyway"
    echo ==========================================
) else (
    echo.
    echo ERROR: Build failed
    echo Check the error messages above
    exit /b 1
)

pause
