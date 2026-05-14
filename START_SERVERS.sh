#!/bin/bash

echo "🚀 AI SQL Copilot - Server Startup Script"
echo "=========================================="
echo ""

# Check Ollama
echo "1️⃣ Checking Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "   ✅ Ollama is running"
else
    echo "   ⚠️  Ollama is not running"
    echo "   Please start Ollama in a separate terminal:"
    echo "   ollama serve"
    echo ""
    read -p "Press Enter to continue anyway..."
fi

# Check Gemma model
echo ""
echo "2️⃣ Checking Gemma:3b model..."
if ollama list 2>/dev/null | grep -q "gemma:3b"; then
    echo "   ✅ Gemma:3b model is available"
else
    echo "   ⚠️  Gemma:3b model not found"
    echo "   Run: ollama pull gemma:3b"
    echo ""
    read -p "Press Enter to continue anyway..."
fi

# Start Backend
echo ""
echo "3️⃣ Starting Backend Server..."
cd backend
source venv/bin/activate
echo "   ✅ Virtual environment activated"
echo "   🚀 Starting Flask server on port 5001..."
echo "   (This will run in the foreground - use Ctrl+C to stop)"
echo ""
python app.py
