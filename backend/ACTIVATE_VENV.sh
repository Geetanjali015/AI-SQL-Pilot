#!/bin/bash
# Quick script to activate virtual environment

if [ -d "venv" ]; then
    echo "✅ Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated!"
    echo ""
    echo "You can now:"
    echo "  - Install dependencies: pip install -r requirements.txt"
    echo "  - Run the server: python app.py"
    echo ""
    echo "To deactivate, run: deactivate"
else
    echo "❌ Virtual environment not found. Creating it now..."
    python3 -m venv venv
    echo "✅ Virtual environment created!"
    echo "Run this script again to activate it."
fi
