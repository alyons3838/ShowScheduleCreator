#!/bin/bash
# Build script for creating Mac application bundle

echo "=========================================="
echo "Building Thousand Hills Schedule Creator"
echo "Mac Application Bundle"
echo "=========================================="
echo ""

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "ERROR: Virtual environment not found."
        echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
        exit 1
    fi
fi

# Ensure PyInstaller is installed
echo "Checking dependencies..."
pip install -q pyinstaller

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist *.spec

# Build the application
echo "Building application bundle..."
echo "This may take a few minutes..."
echo ""

pyinstaller --noconfirm \
    --name="ThousandHillsScheduleCreator" \
    --windowed \
    --onefile \
    --osx-bundle-identifier="com.thousandhills.schedulecreator" \
    --add-data="templates:templates" \
    --add-data="static:static" \
    --hidden-import="pdfplumber" \
    --hidden-import="reportlab" \
    --hidden-import="PIL" \
    --hidden-import="werkzeug" \
    --collect-all="reportlab" \
    --collect-all="pdfplumber" \
    launcher.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Build successful!"
    echo "=========================================="
    echo ""
    echo "Your application is ready at:"
    echo "  dist/ThousandHillsScheduleCreator.app"
    echo ""
    echo "To distribute to your reps:"
    echo "1. Copy the .app file to a USB drive or"
    echo "2. Zip it and send via email/cloud storage"
    echo ""
    echo "Users just need to:"
    echo "1. Copy the app to their Applications folder"
    echo "2. Double-click to run"
    echo ""
    echo "First-time users may need to right-click > Open"
    echo "to bypass macOS Gatekeeper security."
    echo "=========================================="
else
    echo ""
    echo "ERROR: Build failed"
    echo "Check the error messages above"
    exit 1
fi
