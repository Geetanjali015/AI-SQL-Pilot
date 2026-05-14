# 🚀 Quick Start Guide - AI SQL Copilot

Get up and running in 5 minutes!

## Prerequisites Checklist

Before starting, make sure you have:

- [ ] **Python 3.9+** installed (`python3 --version`)
- [ ] **Node.js 18+** installed (`node --version`)
- [ ] **Ollama** installed ([https://ollama.com](https://ollama.com))

## Step-by-Step Setup

### 1️⃣ Install Ollama & Pull Model (5 min)

```bash
# Install Ollama (macOS)
brew install ollama

# Start Ollama service
ollama serve

# In a new terminal, pull the Gemma model
ollama pull gemma:3b

# Verify installation
ollama list
```

### 2️⃣ Automated Setup (2 min)

```bash
# Navigate to project directory
cd /Users/admin92/Desktop/prism

# Make setup script executable and run
chmod +x setup.sh
./setup.sh
```

This will:
- Create Python virtual environment
- Install all backend dependencies
- Generate sample SQLite database
- Install all frontend dependencies

### 3️⃣ Start the Application (1 min)

Open **TWO** terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python app.py
```

Wait for: `Running on http://127.0.0.1:5001`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Wait for: `Local: http://localhost:5173/`

### 4️⃣ Use the Application

1. Open your browser to **http://localhost:5173**
2. Keep default database type as **SQLite**
3. Keep default path as **sample_db.sqlite**
4. Click **"Connect to Database"**
5. Try an example query like: *"Show me all customers who made purchases in the last 30 days"*
6. Click **"Generate & Optimize SQL"**
7. View results, performance metrics, and optimization suggestions!

---

## Manual Setup (Alternative)

If automated setup fails, follow manual steps:

### Backend Setup

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create sample database
python create_sample_db.py

# Start server
python app.py
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

---

## Troubleshooting

### ❌ "Ollama is not running"

```bash
# Start Ollama in a separate terminal
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### ❌ "Port 5001 already in use"

```bash
# Kill process on port 5001
lsof -ti:5001 | xargs kill -9

# Or change port in backend/.env
PORT=5002
```

### ❌ "Cannot connect to database"

- Make sure you're in the `backend` directory
- Check that `sample_db.sqlite` file exists
- Try absolute path: `/Users/admin92/Desktop/prism/backend/sample_db.sqlite`

### ❌ "Module not found" errors

```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## First Query Examples

Try these natural language queries:

1. **Simple**: `"Show me all products"`
2. **Filtered**: `"Find customers who registered in the last 6 months"`
3. **Aggregated**: `"What are the top 5 best-selling products?"`
4. **Complex**: `"Calculate total revenue by region for orders in 2024"`
5. **Joins**: `"Show customer names with their order counts"`

---

## Project URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5001/api
- **Health Check**: http://localhost:5001/api/health
- **Ollama**: http://localhost:11434

---

## Next Steps

✅ Connected to database  
✅ Generated your first SQL query  
✅ Viewed optimization suggestions  

**Now try:**
- Connect to your own database (MySQL/PostgreSQL)
- Explore performance comparisons
- Apply suggested indexes
- Export optimized queries

---

## Need Help?

1. Check `README.md` for full documentation
2. Review backend logs in terminal for errors
3. Verify all services are running (Ollama, Flask, Vite)
4. Check `.env` configuration in backend folder

---

**Ready to optimize SQL with AI! 🚀**
