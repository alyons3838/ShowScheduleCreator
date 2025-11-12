#!/bin/bash
# Simplified start script - use if run.sh doesn't work

echo "Thousand Hills Vacations - Show Schedule Creator"
echo "=================================================="
echo ""

# Try to activate existing venv or create instructions
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "Starting application..."
    python app.py
else
    echo "Virtual environment not found."
    echo ""
    echo "Please run these commands manually:"
    echo ""
    echo "1. python3 -m venv venv"
    echo "2. source venv/bin/activate"
    echo "3. pip install -r requirements.txt"
    echo "4. python app.py"
    echo ""
    echo "Then open: http://127.0.0.1:5000"
fi
