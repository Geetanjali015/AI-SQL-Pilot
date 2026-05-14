# AI SQL Copilot 🤖

> **Production-ready full-stack web application for LLM-powered SQL optimization**

An intelligent SQL assistant that uses **Retrieval-Augmented Generation (RAG)** powered by **Ollama's Gemma:3b** to generate, optimize, and profile SQL queries from natural language.

![AI SQL Copilot](https://img.shields.io/badge/AI-SQL%20Copilot-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-green?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18.2+-61DAFB?style=for-the-badge&logo=react)
![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask)

---

## 🌟 Features

### 🧠 AI-Powered SQL Generation
- Convert natural language queries to SQL using **Ollama Gemma:3b**
- RAG pipeline with **LangChain** for context-aware query generation
- Vector database (**Chroma**) for schema retrieval

### ⚡ Query Optimization
- Automatic SQL query optimization
- Rule-based anti-pattern detection
- LLM-powered optimization suggestions
- Index recommendations based on query patterns

### 📊 Performance Profiling
- Real-time execution time measurement
- Memory and CPU usage tracking
- Query plan analysis with EXPLAIN
- Side-by-side performance comparison

### 🎨 Modern Web Dashboard
- Clean, professional UI with **Tailwind CSS**
- Interactive performance charts with **Recharts**
- Real-time query results display
- Copy-to-clipboard functionality

### 🗄️ Multi-Database Support
- **SQLite** (with included sample database)
- **MySQL/MariaDB**
- **PostgreSQL**

---

## 📦 Project Structure

```
ai-sql-copilot/
├── backend/
│   ├── app.py                      # Flask application entry point
│   ├── requirements.txt            # Python dependencies
│   ├── .env                        # Environment configuration
│   ├── create_sample_db.py        # Sample database generator
│   ├── models/
│   │   └── db_connection.py       # Database connection & schema extraction
│   ├── routes/
│   │   ├── db_routes.py           # Database API endpoints
│   │   ├── llm_routes.py          # LLM & SQL generation endpoints
│   │   └── query_routes.py        # Query execution & profiling endpoints
│   └── services/
│       ├── rag_pipeline.py        # RAG implementation with Ollama
│       ├── sql_profiler.py        # Query performance profiling
│       └── optimizer_agent.py     # Query optimization engine
└── frontend/
    ├── package.json               # Node.js dependencies
    ├── vite.config.js            # Vite configuration
    ├── tailwind.config.js        # Tailwind CSS configuration
    ├── index.html                # HTML entry point
    └── src/
        ├── App.jsx               # Main React component
        ├── main.jsx              # React entry point
        ├── index.css             # Global styles
        ├── api/
        │   └── apiClient.js      # Axios API client
        └── components/
            ├── DatabaseConnect.jsx    # DB connection form
            ├── QueryAssistant.jsx     # Natural language input
            └── ResultsDashboard.jsx   # Results & visualizations
```

---

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.9+**
- **Node.js 18+** and npm
- **Ollama** installed and running locally

### Step 1: Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows - Download from https://ollama.com
```

### Step 2: Pull Gemma Model

```bash
ollama pull gemma:3b
```

Verify Ollama is running:
```bash
ollama list
```

### Step 3: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create sample database (optional but recommended)
python create_sample_db.py

# Start Flask server
python app.py
```

The backend will run on **http://localhost:5001**

### Step 4: Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will run on **http://localhost:5173**

---

## 🎮 Usage

### 1. Connect to Database

- Open **http://localhost:5173** in your browser
- Choose database type: **SQLite**, **MySQL**, or **PostgreSQL**
- For quick demo: Use default SQLite path `sample_db.sqlite`
- Click **Connect to Database**

### 2. Ask Questions in Natural Language

Try these example queries:

- "Show me all customers who made purchases in the last 30 days"
- "What are the top 5 best-selling products?"
- "Calculate total revenue by region"
- "Find customers who haven't made any orders"
- "Show average order value by product category"

### 3. View Results

The dashboard displays:

- **Overview**: Quick stats and performance improvements
- **SQL Queries**: Generated and optimized SQL with copy buttons
- **Performance**: Execution time and memory charts
- **Suggestions**: Issues, optimizations, and index recommendations

---

## 🔧 Configuration

### Backend (.env)

```env
# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
PORT=5001

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma:3b

# Vector Store
VECTOR_STORE_PATH=./vector_store/chroma_index
EMBEDDING_MODEL=all-MiniLM-L6-v2

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (vite.config.js)

```javascript
export default defineConfig({
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
      }
    }
  }
})
```

---

## 🔌 API Endpoints

### Database Operations

- `POST /api/connect-db` - Connect to database
- `GET /api/get-schema` - Get current schema
- `POST /api/disconnect-db` - Disconnect database

### LLM Operations

- `POST /api/generate-sql` - Generate SQL from natural language
- `POST /api/optimize-query` - Optimize SQL query
- `POST /api/analyze-query` - Analyze query for issues
- `POST /api/get-suggestions` - Get optimization suggestions

### Query Operations

- `POST /api/run-query` - Execute and profile query
- `POST /api/compare-queries` - Compare two queries
- `POST /api/profile-query` - Profile query without full results
- `GET /api/system-metrics` - Get system performance metrics

### Health Check

- `GET /api/health` - Server health check

---

## 📊 Sample Database Schema

The included SQLite database contains e-commerce data:

**Tables:**
- `regions` - Geographic regions
- `customers` - Customer information
- `categories` - Product categories
- `products` - Product catalog
- `orders` - Order history
- `order_items` - Order line items

**Sample Data:**
- 7 regions
- 100 customers
- 7 categories
- 25 products
- 200+ orders

---

## 🛠️ Technologies Used

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **LangChain** - LLM orchestration
- **Ollama** - Local LLM inference
- **Chroma** - Vector database
- **Sentence Transformers** - Embeddings
- **psutil** - System metrics

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Recharts** - Data visualization
- **Lucide React** - Icons

---

## 🐛 Troubleshooting

### Ollama Not Running

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

### Port Already in Use

```bash
# Backend (change port in .env file or use environment variable)
PORT=5002 python app.py

# Frontend (change in vite.config.js)
npm run dev -- --port 5174
```

### Database Connection Failed

- **SQLite**: Ensure `sample_db.sqlite` exists in backend directory
- **MySQL/PostgreSQL**: Verify credentials and database exists
- Check firewall settings for remote connections

### Vector Store Errors

```bash
# Clear vector store
rm -rf backend/vector_store/chroma_index

# Reconnect to database to rebuild index
```

### CORS Issues

Ensure `CORS_ORIGINS` in `.env` matches your frontend URL

---

## 📈 Performance Tips

1. **Use Indexes**: Apply suggested indexes for faster queries
2. **Limit Results**: Add LIMIT clauses for large datasets
3. **Avoid SELECT ***: Specify only needed columns
4. **Use Query Cache**: Ollama caches LLM responses
5. **Optimize Joins**: Use explicit JOIN syntax

---

## 🔐 Security Notes

⚠️ **Important**: This is a development setup. For production:

- Change `SECRET_KEY` in `.env`
- Use environment variables for sensitive data
- Enable authentication/authorization
- Implement rate limiting
- Use HTTPS
- Validate and sanitize all inputs
- Restrict database permissions

---

## 📝 License

MIT License - feel free to use this project for learning or commercial purposes.

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Support for more databases (MongoDB, MS SQL Server)
- Query result caching
- User authentication
- Query history and favorites
- Export results to CSV/JSON
- Dark/light theme toggle
- Multi-language support

---

## 📧 Support

For issues and questions:
- Check the troubleshooting section
- Review API logs in terminal
- Verify Ollama is running correctly

---

## 🎯 Key Highlights

✅ **Production-Ready**: Modular architecture, error handling, logging  
✅ **RAG Pipeline**: Context-aware SQL generation with vector retrieval  
✅ **Performance Metrics**: Real-time profiling and comparison  
✅ **Modern UI**: Clean dashboard with interactive visualizations  
✅ **Multi-Database**: SQLite, MySQL, PostgreSQL support  
✅ **LLM-Powered**: Ollama Gemma:3b for local inference  
✅ **Fully Documented**: Comprehensive comments and README  

---

**Built with ❤️ using Ollama, LangChain, Flask, and React**

*Happy querying! 🚀*
