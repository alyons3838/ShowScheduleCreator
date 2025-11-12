#!/bin/bash
# Quick start script for Mac/Linux

echo "=========================================="
echo "Thousand Hills Vacations"
echo "Show Schedule Creator"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Please install Python 3.8 or higher:"
    echo "  - Via Homebrew: brew install python3"
    echo "  - Or download from: https://www.python.org/downloads/"
    exit 1
fi

echo "Python version: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    if ! python3 -m venv venv; then
        echo "ERROR: Failed to create virtual environment."
        echo "Try: python3 -m pip install --user virtualenv"
        exit 1
    fi
    echo "Virtual environment created successfully."
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "ERROR: Could not find venv/bin/activate"
    echo "Try deleting the venv folder and running again:"
    echo "  rm -rf venv"
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install/update dependencies
echo "Installing dependencies..."
if ! pip install -r requirements.txt; then
    echo ""
    echo "ERROR: Failed to install dependencies."
    echo "Try manually with: pip install -r requirements.txt"
    exit 1
fi

echo "Dependencies installed successfully."

# Run the application
echo ""
echo "=========================================="
echo "Starting application..."
echo "=========================================="
echo ""
echo "Open your browser to: http://127.0.0.1:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
