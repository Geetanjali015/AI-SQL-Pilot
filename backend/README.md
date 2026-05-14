# AI SQL Copilot - Backend

Production-ready Flask backend for AI SQL Copilot.

## Quick Start

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create sample database
python create_sample_db.py

# Run server
python app.py
```

## Project Structure

- `app.py` - Main Flask application
- `models/` - Database models and connections
- `routes/` - API endpoints
- `services/` - Business logic (RAG, profiling, optimization)
- `vector_store/` - Chroma vector database (auto-created)

## API Documentation

### Database Routes (`/api`)
- `POST /connect-db` - Connect to database
- `GET /get-schema` - Get schema information
- `POST /disconnect-db` - Disconnect database

### LLM Routes (`/api`)
- `POST /generate-sql` - Generate SQL from natural language
- `POST /optimize-query` - Optimize SQL query
- `POST /analyze-query` - Analyze query for issues

### Query Routes (`/api`)
- `POST /run-query` - Execute and profile query
- `POST /compare-queries` - Compare two queries

## Environment Variables

See `.env.example` for configuration options.

## Requirements

- Python 3.9+
- Ollama with Gemma:3b model
- SQLite/MySQL/PostgreSQL
