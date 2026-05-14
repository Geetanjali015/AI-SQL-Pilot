#!/bin/bash

echo "🚀 Starting Frontend Server"
echo "============================"
echo ""

cd /Users/aryanbhutyal/prism_new/frontend

echo "📦 Checking dependencies..."
if [ ! -d "node_modules" ]; then
    echo "   Installing dependencies..."
    npm install
else
    echo "   ✅ Dependencies already installed"
fi

echo ""
echo "🌐 Starting Vite development server..."
echo "   Server will run on: http://localhost:5173"
echo "   Press Ctrl+C to stop the server"
echo ""

npm run dev



