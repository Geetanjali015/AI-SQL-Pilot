# 🧠 RAG Pipeline: Data Dictionary & Chroma DB Usage

## ✅ Yes! The system uses both Data Dictionary and Chroma DB for context

Here's exactly how it works:

---

## 📊 Step 1: Database Connection & Indexing

When you connect to a database, the system:

### 1.1 Extracts Schema
- Tables and their columns
- Column types, nullable status
- Primary keys and foreign keys
- Relationships between tables

### 1.2 Generates Comprehensive Data Dictionary
The data dictionary includes:
- **Table Information**: Name, description, row count
- **Column Details**: 
  - Name, type, nullable
  - Primary key status
  - Foreign key status
  - Unique value count (cardinality)
  - **Sample values** (up to 5 distinct values per column)
- **Sample Data**: First 3 rows from each table
- **Relationships**: Foreign key mappings
- **Query Guidelines**: Instructions for the LLM

### 1.3 Formats for LLM Context
The `format_data_dictionary_for_llm()` method creates a comprehensive text document like:

```
=== DATABASE INFORMATION ===
Database Type: sqlite
Total Tables: 6

=== DETAILED TABLE SCHEMAS ===

TABLE: customers
Description: Table containing customers records
Row Count: 100
Primary Keys: id

COLUMNS:
  • id
    - Type: INTEGER
    - Nullable: No
    - Primary Key: Yes
    - Foreign Key: No
    - Unique Values: 100
    - Sample Values: 1, 2, 3

  • name
    - Type: VARCHAR(100)
    - Nullable: No
    - Primary Key: No
    - Foreign Key: No
    - Unique Values: 95
    - Sample Values: John Doe, Jane Smith, Bob Johnson

  ...

SAMPLE DATA (first 3 rows):
  Row 1: {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', ...}
  Row 2: {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', ...}
  Row 3: {'id': 3, 'name': 'Bob Johnson', 'email': 'bob@example.com', ...}

FOREIGN KEY RELATIONSHIPS:
  • customer_id references orders(id)
  ...
```

### 1.4 Stores in Chroma DB
The system stores three types of data in Chroma DB:

1. **Schema Chunks** (type: "schema")
   - The formatted data dictionary text is split into chunks
   - Each chunk is ~800 characters with 100 character overlap
   - Each chunk is embedded using Sentence Transformers
   - Stored with metadata `{"type": "schema", "chunk_index": i}`

2. **Complete Schema JSON** (type: "complete_schema")
   - The entire schema as structured JSON
   - Stored for reference

3. **Data Dictionary JSON** (type: "data_dictionary")
   - The complete data dictionary as JSON
   - Includes all sample values and metadata

---

## 🔍 Step 2: Query Generation (RAG Retrieval)

When you ask a natural language question:

### 2.1 Query Embedding
```python
# User query: "Show me all customers who made purchases in the last 30 days"
query_embedding = embedding_model.encode([query])
```

### 2.2 Semantic Search in Chroma DB
```python
# Search for top 5 most relevant schema chunks
results = chroma_collection.query(
    query_embeddings=[query_embedding],
    n_results=5,  # top_k=5
    where={"type": "schema"}  # Only search schema chunks
)
```

### 2.3 Context Retrieval
The system retrieves the **5 most relevant chunks** from the data dictionary based on semantic similarity to your query.

For example, if you ask about "customers" and "purchases", it might retrieve:
- Chunks about the `customers` table
- Chunks about the `orders` table
- Chunks about the relationship between customers and orders
- Chunks with sample data showing customer order patterns

### 2.4 SQL Generation
The retrieved context is passed to the LLM along with your query:

```python
prompt = f"""
Database Schema Context:
{retrieved_schema_context}  # Top 5 relevant chunks from data dictionary

Natural Language Query: {your_query}

Generate optimized SQL query...
"""
```

---

## 🎯 Key Features

### ✅ Semantic Search
- Uses vector embeddings to find **relevant** schema information
- Not just keyword matching - understands **meaning**
- Example: Query about "users" will find "customers" table if semantically similar

### ✅ Sample Data Context
- The data dictionary includes **sample values** from columns
- Helps LLM understand:
  - Data types and formats
  - Value patterns
  - Relationships
  - Example: If a column has values like "2024-01-15", LLM knows it's a date

### ✅ Relationship Awareness
- Foreign key relationships are included
- Helps LLM create proper JOINs
- Example: Knows that `orders.customer_id` → `customers.id`

### ✅ Row Counts & Cardinality
- Table row counts help with optimization
- Unique value counts show data distribution
- Helps LLM choose efficient query strategies

---

## 📈 Benefits of This Approach

1. **Context-Aware**: Only retrieves relevant schema parts, not everything
2. **Efficient**: Top 5 chunks instead of full schema (faster, less tokens)
3. **Accurate**: Sample data helps LLM understand actual data patterns
4. **Relationship-Aware**: Knows how tables connect
5. **Optimized**: Row counts and cardinality inform optimization decisions

---

## 🔧 Configuration

### Chroma DB Settings
- **Chunk Size**: 800 characters
- **Chunk Overlap**: 100 characters
- **Top K Results**: 5 chunks
- **Embedding Model**: `all-MiniLM-L6-v2` (Sentence Transformers)

### Data Dictionary Includes
- ✅ Table schemas
- ✅ Column details
- ✅ Sample values (5 per column)
- ✅ Sample rows (3 per table)
- ✅ Row counts
- ✅ Unique value counts
- ✅ Foreign key relationships
- ✅ Primary keys
- ✅ Data types

---

## 🚀 Example Flow

### User Query:
"Show me all customers who made purchases in the last 30 days"

### System Process:
1. **Embed Query**: Convert to vector embedding
2. **Search Chroma DB**: Find top 5 relevant schema chunks
   - Might retrieve: customers table, orders table, order_items table, relationships
3. **Retrieve Context**: Get chunks with:
   - Customer table structure
   - Order table structure
   - Relationship: orders.customer_id → customers.id
   - Sample data showing date formats
4. **Generate SQL**: LLM uses context to generate:
   ```sql
   SELECT DISTINCT c.id, c.name, c.email
   FROM customers c
   INNER JOIN orders o ON c.id = o.customer_id
   WHERE o.order_date >= date('now', '-30 days')
   ```
5. **Return Result**: Optimized SQL with proper JOINs and filtering

---

## 🎓 Summary

**Yes, the system uses:**
- ✅ **Data Dictionary**: Comprehensive schema with sample data
- ✅ **Chroma DB**: Vector database for semantic search
- ✅ **Embeddings**: Sentence Transformers for similarity search
- ✅ **RAG**: Retrieval-Augmented Generation pattern

**The flow:**
1. Store data dictionary in Chroma DB (chunked)
2. Embed user query
3. Retrieve top 5 relevant chunks
4. Use chunks as context for LLM
5. Generate optimized SQL

This ensures the LLM has **relevant, contextual information** about your database schema and data patterns when generating SQL queries!


