# 🐍 Virtual Environment Setup Guide

## ✅ Virtual Environment Created

The virtual environment has been created in the `backend` directory.

---

## 🚀 Quick Start

### Option 1: Manual Activation

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Option 2: Using Setup Script

```bash
cd backend
chmod +x setup.sh
./setup.sh
```

This will:
- Create virtual environment (if it doesn't exist)
- Activate it
- Upgrade pip
- Install all dependencies
- Create sample database
- Check Ollama status

### Option 3: Using Quick Activation Script

```bash
cd backend
source ACTIVATE_VENV.sh
```

---

## 📋 Step-by-Step Instructions

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python --version  # Should show Python 3.9+
pip list  # Should show all installed packages
```

### 5. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5001`

---

## 🔧 Virtual Environment Commands

### Activate Virtual Environment
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Check if Virtual Environment is Active
```bash
which python  # Should point to venv/bin/python
```

### Install New Package
```bash
pip install package-name
pip freeze > requirements.txt  # Update requirements.txt
```

### Remove Virtual Environment
```bash
deactivate  # First deactivate
rm -rf venv  # Then remove directory
```

---

## 📦 Dependencies

All dependencies are listed in `requirements.txt`:

- Flask 3.0.0
- Flask-CORS 4.0.0
- SQLAlchemy 2.0.23
- langchain 0.1.0
- chromadb 0.4.22
- sentence-transformers 2.2.2
- ollama 0.1.6
- psutil 5.9.6
- And more...

---

## ⚠️ Troubleshooting

### Virtual Environment Not Found

```bash
# Create it manually
python3 -m venv venv
source venv/bin/activate
```

### Permission Denied

```bash
# Make scripts executable
chmod +x setup.sh
chmod +x ACTIVATE_VENV.sh
```

### Python Version Issues

```bash
# Check Python version
python3 --version  # Should be 3.9 or higher

# Use specific Python version
python3.9 -m venv venv
```

### pip Install Fails

```bash
# Upgrade pip first
pip install --upgrade pip

# Install dependencies one by one if needed
pip install Flask==3.0.0
pip install Flask-CORS==4.0.0
# etc...
```

---

## 🎯 Next Steps

1. ✅ Virtual environment created
2. ⏭️ Activate virtual environment
3. ⏭️ Install dependencies
4. ⏭️ Start the server
5. ⏭️ Test the application

---

## 📝 Notes

- The virtual environment is in the `backend/venv` directory
- Always activate the virtual environment before running the server
- Dependencies are isolated to this virtual environment
- The `.gitignore` file should exclude `venv/` directory

---

*Virtual environment setup complete! 🎉*


