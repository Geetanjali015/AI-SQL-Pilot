#!/bin/bash

# AI SQL Copilot - Complete Setup Script
# This script sets up both backend and frontend

echo "🚀 AI SQL Copilot - Complete Setup"
echo "===================================="
echo ""

# Setup Backend
echo "🔧 Setting up Backend..."
echo ""
cd backend
chmod +x setup.sh
./setup.sh

if [ $? -ne 0 ]; then
    echo "❌ Backend setup failed"
    exit 1
fi

cd ..
echo ""

# Setup Frontend
echo "🔧 Setting up Frontend..."
echo ""
cd frontend
chmod +x setup.sh
./setup.sh

if [ $? -ne 0 ]; then
    echo "❌ Frontend setup failed"
    exit 1
fi

cd ..
echo ""

echo "✅ Complete setup finished!"
echo ""
echo "📝 Next steps:"
echo "  1. Make sure Ollama is running: ollama serve"
echo "  2. Start backend (in terminal 1):"
echo "     cd backend && source venv/bin/activate && python app.py"
echo "  3. Start frontend (in terminal 2):"
echo "     cd frontend && npm run dev"
echo "  4. Open http://localhost:5173 in your browser"
echo ""
echo "Happy coding! 🎉"
