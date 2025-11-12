#!/bin/bash
# Quick start script for Mac/Linux

echo "=========================================="
echo "Thousand Hills Vacations"
echo "Show Schedule Creator"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run the application
echo ""
echo "Starting application..."
echo "Open your browser to: http://127.0.0.1:5000"
echo "Press Ctrl+C to stop"
echo ""
python app.py
