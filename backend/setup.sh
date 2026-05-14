#!/bin/bash

# AI SQL Copilot - Backend Setup Script
# This script sets up the Python backend environment

echo "🚀 AI SQL Copilot - Backend Setup"
echo "=================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment."
    exit 1
fi

echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies."
    exit 1
fi

echo "✅ Dependencies installed successfully"
echo ""

# Check if Ollama is running
echo "🤖 Checking Ollama..."
curl -s http://localhost:11434/api/tags > /dev/null

if [ $? -ne 0 ]; then
    echo "⚠️  Ollama is not running or not installed."
    echo "   Please install Ollama from: https://ollama.com"
    echo "   Then run: ollama pull gemma:3b"
else
    echo "✅ Ollama is running"
fi

echo ""

# Create sample database
echo "📊 Creating sample database..."
python create_sample_db.py

if [ $? -ne 0 ]; then
    echo "⚠️  Failed to create sample database (non-critical)"
else
    echo "✅ Sample database created: sample_db.sqlite"
fi

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "To start the backend server:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run server: python app.py"
echo ""
echo "The server will be available at: http://localhost:5001"
