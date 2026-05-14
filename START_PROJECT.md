# 🚀 Starting the AI SQL Copilot Project

## Quick Start Guide

### Prerequisites Check

Before starting, ensure you have:

1. ✅ **Ollama installed** and running
2. ✅ **Gemma:3b model** downloaded
3. ✅ **Virtual environment** created and activated
4. ✅ **Dependencies** installed

---

## 📋 Step-by-Step Startup

### Step 1: Start Ollama (Required)

**In Terminal 1:**
```bash
# Start Ollama service
ollama serve
```

**In Terminal 2 (new terminal):**
```bash
# Pull Gemma model (if not already done)
ollama pull gemma:3b

# Verify model is available
ollama list
```

### Step 2: Start Backend Server

**In Terminal 3 (new terminal):**
```bash
cd /Users/aryanbhutyal/prism_new/backend

# Activate virtual environment
source venv/bin/activate

# Start Flask server
python app.py
```

You should see:
```
Starting Flask server on port 5001
Running on http://127.0.0.1:5001
```

### Step 3: Start Frontend Server

**In Terminal 4 (new terminal):**
```bash
cd /Users/aryanbhutyal/prism_new/frontend

# Install dependencies (if not done)
npm install

# Start development server
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### Step 4: Open Application

Open your browser and go to:
**http://localhost:5173**

---

## 🔍 Verification

### Check Backend
```bash
curl http://localhost:5001/api/health
```

Should return:
```json
{"status": "healthy", "message": "AI SQL Copilot API is running"}
```

### Check Ollama
```bash
curl http://localhost:11434/api/tags
```

Should return list of available models.

### Check Frontend
Open browser to: http://localhost:5173

---

## ⚠️ Common Issues

### Ollama Not Running
```bash
# Start Ollama
ollama serve

# In another terminal, verify
curl http://localhost:11434/api/tags
```

### Gemma Model Not Found
```bash
# Pull the model
ollama pull gemma:3b

# Verify
ollama list
```

### Port Already in Use

**Backend (port 5001):**
```bash
# Kill process on port 5001
lsof -ti:5001 | xargs kill -9

# Or change port in .env
PORT=5002
```

**Frontend (port 5173):**
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9

# Or change in vite.config.js
```

### Virtual Environment Not Activated
```bash
cd backend
source venv/bin/activate
# You should see (venv) in your prompt
```

### Dependencies Not Installed
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📊 Current Status

### ✅ Completed
- Virtual environment created
- Dependencies installed
- Sample database created
- Backend server starting...

### ⚠️ Action Required
- **Gemma:3b model**: Run `ollama pull gemma:3b` if not already done
- **Ollama service**: Ensure `ollama serve` is running

---

## 🎯 All Services Running

Once everything is started, you should have:

1. ✅ **Ollama**: Running on port 11434
2. ✅ **Backend**: Running on port 5001
3. ✅ **Frontend**: Running on port 5173

Then you can:
- Connect to database
- Generate SQL queries
- View performance metrics
- Get optimization suggestions

---

## 🛑 Stopping Services

### Stop Backend
Press `Ctrl+C` in the backend terminal

### Stop Frontend
Press `Ctrl+C` in the frontend terminal

### Stop Ollama
Press `Ctrl+C` in the Ollama terminal (or it may run as a service)

---

*Happy querying! 🚀*


