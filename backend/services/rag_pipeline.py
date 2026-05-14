"""
RAG Pipeline Service
====================
Implements Retrieval-Augmented Generation using Ollama and LangChain.
Stores schema information in Chroma vector database for context retrieval.
"""

import os
import logging
from typing import Dict, List, Any
import chromadb
from chromadb.config import Settings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import json
import re

logger = logging.getLogger(__name__)

# Import db_connection for schema access
try:
    from models.db_connection import db_connection
except ImportError:
    db_connection = None
    logger.warning("Could not import db_connection - example query generation may be limited")


class RAGService:
    """Handles RAG pipeline for SQL generation using Ollama and Chroma"""
    
    def __init__(self):
        self.ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'gemma3:4b')
        self.vector_store_path = os.getenv('VECTOR_STORE_PATH', './vector_store/chroma_index')
        
        # Initialize Ollama LLM
        try:
            self.llm = Ollama(
                base_url=self.ollama_base_url,
                model=self.ollama_model,
                temperature=0.1  # Low temperature for more deterministic SQL generation
            )
            logger.info(f"Initialized Ollama with model: {self.ollama_model}")
        except Exception as e:
            logger.error(f"Failed to initialize Ollama: {str(e)}")
            self.llm = None
        
        # Initialize Chroma vector store
        try:
            self.chroma_client = chromadb.PersistentClient(
                path=self.vector_store_path,
                settings=Settings(anonymized_telemetry=False)
            )
            self.collection = self.chroma_client.get_or_create_collection(
                name="database_schema",
                metadata={"description": "Database schema information for SQL generation"}
            )
            logger.info("Initialized Chroma vector store")
        except Exception as e:
            logger.error(f"Failed to initialize Chroma: {str(e)}")
            self.chroma_client = None
            self.collection = None
        
        # Initialize embedding model
        try:
            embedding_model = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
            self.embedding_model = SentenceTransformer(embedding_model)
            logger.info(f"Initialized embedding model: {embedding_model}")
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {str(e)}")
            self.embedding_model = None
        
        # SQL generation prompt template (optimized version)
        self.sql_generation_prompt = PromptTemplate(
            input_variables=["natural_query", "schema_context", "database_type"],
            template="""You are an expert SQL query generator specializing in creating highly optimized, production-ready SQL queries.
Given a natural language query and database schema context, generate an OPTIMIZED SQL query.

Database Type: {database_type}

Database Schema Context:
{schema_context}

Natural Language Query: {natural_query}

CRITICAL OPTIMIZATION REQUIREMENTS:
1. Use ONLY table and column names that exist in the schema above - verify before including
2. Select ONLY necessary columns (never use SELECT *) to reduce data transfer
3. Use appropriate JOINs with optimal order (smaller tables first when possible)
4. Add WHERE clauses for filtering early in the query
5. Use proper indexes (consider columns used in WHERE, JOIN, ORDER BY clauses)
6. Avoid subqueries where JOINs are more efficient
7. Use aggregate functions efficiently with proper GROUP BY
8. Ensure the query is syntactically correct for {database_type}
9. Use explicit JOIN syntax (INNER JOIN, LEFT JOIN) instead of comma-separated tables
10. Consider query performance and readability

Return ONLY the SQL query without any explanations, markdown formatting, or code blocks.
Just the raw SQL query.

SQL Query:"""
        )
        
        # Query optimization prompt template
        self.optimization_prompt = PromptTemplate(
            input_variables=["original_query", "schema_context"],
            template="""You are an expert SQL query optimizer. Analyze the following SQL query and create an optimized version.

Database Schema Context:
{schema_context}

Original SQL Query:
{original_query}

OPTIMIZATION TASKS:
1. Identify inefficiencies in the original query (e.g., SELECT *, missing indexes, suboptimal JOINs)
2. Rewrite the query with performance improvements
3. Ensure the optimized query returns the same logical results
4. Specify only necessary columns instead of SELECT *
5. Optimize JOIN order based on table sizes and relationships
6. Add appropriate indexes recommendations
7. Use EXPLAIN to understand query execution plans

CRITICAL: Use ONLY table and column names from the schema context above.

Format your response EXACTLY as this JSON (no markdown, no extra text):
{{
    "optimized_query": "the optimized SQL query here",
    "optimizations_applied": ["specific optimization 1", "specific optimization 2", "specific optimization 3"],
    "explanation": "Clear explanation of why these optimizations improve performance"
}}

Response:"""
        )
    
    def index_schema(self, schema_text: str, schema_dict: Dict, data_dictionary: Dict = None) -> Dict:
        """
        Index database schema and data dictionary in vector store
        
        Args:
            schema_text (str): Human-readable schema description with data dictionary
            schema_dict (dict): Structured schema information
            data_dictionary (dict): Optional comprehensive data dictionary
        
        Returns:
            dict: Indexing status
        """
        if not self.collection or not self.embedding_model:
            return {
                'success': False,
                'message': 'Vector store not initialized'
            }
        
        try:
            # Clear existing schema documents
            try:
                self.collection.delete(where={"type": "schema"})
                self.collection.delete(where={"type": "complete_schema"})
                self.collection.delete(where={"type": "data_dictionary"})
            except:
                pass  # Collection might be empty
            
            # Split comprehensive schema text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,  # Larger chunks for more context
                chunk_overlap=100,
                separators=["\n\n", "\n", " ", ""]
            )
            
            chunks = text_splitter.split_text(schema_text)
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(chunks).tolist()
            
            # Create IDs and metadata
            ids = [f"schema_chunk_{i}" for i in range(len(chunks))]
            metadatas = [{"type": "schema", "chunk_index": i} for i in range(len(chunks))]
            
            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
            
            # Store complete schema as JSON
            schema_json = json.dumps(schema_dict, indent=2)
            schema_embedding = self.embedding_model.encode([schema_json]).tolist()
            
            self.collection.add(
                ids=["complete_schema"],
                embeddings=schema_embedding,
                documents=[schema_json],
                metadatas=[{"type": "complete_schema"}]
            )
            
            # Store data dictionary if available
            if data_dictionary:
                data_dict_json = json.dumps(data_dictionary, indent=2)
                dict_embedding = self.embedding_model.encode([data_dict_json]).tolist()
                
                self.collection.add(
                    ids=["data_dictionary"],
                    embeddings=dict_embedding,
                    documents=[data_dict_json],
                    metadatas=[{"type": "data_dictionary"}]
                )
                logger.info("Data dictionary stored in vector database")
            
            logger.info(f"Indexed {len(chunks)} schema chunks in vector store")
            
            return {
                'success': True,
                'message': f'Indexed {len(chunks)} schema chunks with data dictionary',
                'chunk_count': len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Error indexing schema: {str(e)}")
            return {
                'success': False,
                'message': f'Indexing failed: {str(e)}'
            }
    
    def retrieve_relevant_schema(self, query: str, top_k: int = 5) -> str:
        """
        Retrieve relevant schema context for a natural language query
        
        Args:
            query (str): Natural language query
            top_k (int): Number of relevant chunks to retrieve
        
        Returns:
            str: Relevant schema context
        """
        if not self.collection or not self.embedding_model:
            return ""
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query]).tolist()[0]
            
            # Query vector store
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where={"type": "schema"}
            )
            
            if results and results['documents']:
                relevant_context = "\n\n".join(results['documents'][0])
                return relevant_context
            
            return ""
            
        except Exception as e:
            logger.error(f"Error retrieving schema context: {str(e)}")
            return ""
    
    def generate_sql(self, natural_query: str, database_type: str = "sqlite") -> Dict:
        """
        Generate SQL query from natural language using RAG
        
        Args:
            natural_query (str): Natural language query
            database_type (str): Type of database (mysql, postgresql, sqlite)
        
        Returns:
            dict: Generated SQL query and metadata
        """
        if not self.llm:
            return {
                'success': False,
                'message': 'Ollama LLM not initialized. Please ensure Ollama is running.'
            }
        
        try:
            # Retrieve relevant schema context
            schema_context = self.retrieve_relevant_schema(natural_query)
            
            if not schema_context:
                schema_context = "No schema context available. Generate a generic query."
            
            # Generate SQL using LLM
            chain = LLMChain(llm=self.llm, prompt=self.sql_generation_prompt)
            
            response = chain.run(
                natural_query=natural_query,
                schema_context=schema_context,
                database_type=database_type
            )
            
            # Clean up the response
            generated_sql = response.strip()
            
            # Remove markdown code blocks if present
            if generated_sql.startswith("```sql"):
                generated_sql = generated_sql[6:]
            if generated_sql.startswith("```"):
                generated_sql = generated_sql[3:]
            if generated_sql.endswith("```"):
                generated_sql = generated_sql[:-3]
            
            generated_sql = generated_sql.strip()
            
            logger.info(f"Generated SQL query for: {natural_query}")
            
            return {
                'success': True,
                'generated_sql': generated_sql,
                'schema_context_used': schema_context[:200] + "..."  # First 200 chars for reference
            }
            
        except Exception as e:
            logger.error(f"Error generating SQL: {str(e)}")
            return {
                'success': False,
                'message': f'SQL generation failed: {str(e)}'
            }
    
    def optimize_query(self, original_query: str, schema_context: str = "") -> Dict:
        """
        Optimize an existing SQL query
        
        Args:
            original_query (str): Original SQL query
            schema_context (str): Database schema context
        
        Returns:
            dict: Optimized query and suggestions
        """
        if not self.llm:
            return {
                'success': False,
                'message': 'Ollama LLM not initialized'
            }
        
        try:
            # If no schema context provided, try to retrieve it
            if not schema_context:
                schema_context = self.retrieve_relevant_schema(original_query)
            
            # Generate optimization suggestions
            chain = LLMChain(llm=self.llm, prompt=self.optimization_prompt)
            
            response = chain.run(
                original_query=original_query,
                schema_context=schema_context
            )
            
            # Try to parse JSON response
            try:
                # Clean response
                response = response.strip()
                if response.startswith("```json"):
                    response = response[7:]
                if response.startswith("```"):
                    response = response[3:]
                if response.endswith("```"):
                    response = response[:-3]
                response = response.strip()
                
                optimization_data = json.loads(response)
                
                return {
                    'success': True,
                    'optimized_query': optimization_data.get('optimized_query', original_query),
                    'optimizations_applied': optimization_data.get('optimizations_applied', []),
                    'explanation': optimization_data.get('explanation', '')
                }
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw response
                logger.warning("Could not parse optimization response as JSON")
                return {
                    'success': True,
                    'optimized_query': original_query,
                    'optimizations_applied': [],
                    'explanation': response
                }
            
        except Exception as e:
            logger.error(f"Error optimizing query: {str(e)}")
            return {
                'success': False,
                'message': f'Query optimization failed: {str(e)}'
            }
    
    def generate_optimized_sql(self, natural_query: str, database_type: str = "sqlite", schema_context: str = "") -> Dict:
        """
        Generate an optimized SQL query directly from natural language
        This method generates the best possible query without intermediate non-optimal steps
        
        Args:
            natural_query (str): Natural language query
            database_type (str): Type of database (mysql, postgresql, sqlite)
            schema_context (str): Database schema context
        
        Returns:
            dict: Optimized SQL query with explanations
        """
        if not self.llm:
            return {
                'success': False,
                'message': 'Ollama LLM not initialized. Please ensure Ollama is running.'
            }
        
        try:
            # Retrieve relevant schema context if not provided
            if not schema_context:
                schema_context = self.retrieve_relevant_schema(natural_query)
            
            if not schema_context:
                schema_context = "No schema context available. Generate a generic query."
            
            # Create optimized generation prompt
            optimized_generation_prompt = PromptTemplate(
                input_variables=["natural_query", "schema_context", "database_type"],
                template="""You are an expert SQL query generator specializing in creating highly optimized queries.
Given a natural language query and database schema, generate an OPTIMIZED, production-ready SQL query.

Database Type: {database_type}

Database Schema Context:
{schema_context}

Natural Language Query: {natural_query}

CRITICAL OPTIMIZATION REQUIREMENTS:
1. Use ONLY table and column names that exist in the schema above
2. Select ONLY necessary columns (never use SELECT *)
3. Use appropriate JOINs with optimal order (smaller tables first)
4. Add WHERE clauses for filtering early in the query
5. Use indexes where available (check schema for indexed columns)
6. Avoid subqueries where JOINs are more efficient
7. Use aggregate functions efficiently with proper GROUP BY
8. Ensure the query is syntactically correct for {database_type}

Format your response EXACTLY as this JSON (no markdown, no extra text):
{{
    "optimized_query": "the optimized SQL query here",
    "optimizations_applied": ["specific optimization 1", "specific optimization 2"],
    "explanation": "Brief explanation of optimization choices",
    "suggested_indexes": ["index suggestions if applicable"]
}}

Response:"""
            )
            
            # Generate optimized SQL
            chain = LLMChain(llm=self.llm, prompt=optimized_generation_prompt)
            
            response = chain.run(
                natural_query=natural_query,
                schema_context=schema_context,
                database_type=database_type
            )
            
            # Try to parse JSON response
            try:
                # Clean response
                response = response.strip()
                if response.startswith("```json"):
                    response = response[7:]
                if response.startswith("```"):
                    response = response[3:]
                if response.endswith("```"):
                    response = response[:-3]
                response = response.strip()
                
                result_data = json.loads(response)
                
                logger.info(f"Generated optimized SQL query for: {natural_query}")
                
                return {
                    'success': True,
                    'optimized_query': result_data.get('optimized_query', ''),
                    'optimizations_applied': result_data.get('optimizations_applied', []),
                    'explanation': result_data.get('explanation', ''),
                    'suggested_indexes': result_data.get('suggested_indexes', [])
                }
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract SQL from plain text
                logger.warning("Could not parse response as JSON, extracting SQL")
                sql_query = response.strip()
                
                # Remove markdown code blocks if present
                if sql_query.startswith("```sql"):
                    sql_query = sql_query[6:]
                if sql_query.startswith("```"):
                    sql_query = sql_query[3:]
                if sql_query.endswith("```"):
                    sql_query = sql_query[:-3]
                sql_query = sql_query.strip()
                
                return {
                    'success': True,
                    'optimized_query': sql_query,
                    'optimizations_applied': ['Direct optimization applied'],
                    'explanation': 'Query generated with optimization best practices',
                    'suggested_indexes': []
                }
            
        except Exception as e:
            logger.error(f"Error generating optimized SQL: {str(e)}")
            return {
                'success': False,
                'message': f'Optimized SQL generation failed: {str(e)}'
            }


    def generate_example_queries(self, count: int = 5) -> Dict:
        """
        Generate example natural language queries based on the database schema
        
        Args:
            count (int): Number of example queries to generate (default: 5)
        
        Returns:
            dict: List of example queries relevant to the database schema
        """
        if not self.llm:
            return {
                'success': False,
                'message': 'Ollama LLM not initialized. Please ensure Ollama is running.'
            }
        
        try:
            # Get full schema context
            schema_context = ""
            try:
                if db_connection.schema_info:
                    schema_context = db_connection.generate_schema_text()
            except Exception as e:
                logger.warning(f"Could not get schema context: {str(e)}")
            
            if not schema_context:
                # Fallback to basic schema info
                if db_connection.schema_info:
                    tables = db_connection.schema_info.get('tables', [])
                    table_names = [t['name'] for t in tables]
                    schema_context = f"Database has {len(table_names)} tables: {', '.join(table_names)}"
                else:
                    schema_context = "No schema information available"
            
            # Create prompt for generating example queries
            example_queries_prompt = PromptTemplate(
                input_variables=["schema_context", "count"],
                template="""You are an expert at creating natural language queries for SQL databases.

Database Schema:
{schema_context}

Generate exactly {count} diverse, realistic natural language queries that would be useful for this database.
The queries should:
1. Use actual table and column names from the schema above
2. Be practical and useful (not generic)
3. Cover different types of queries (SELECT, aggregations, joins, filters, etc.)
4. Be written in natural, conversational language
5. Be specific to the data in this database

Return ONLY a JSON array of strings, one query per string. No markdown, no explanation, just the array.

Example format:
["Show me all customers from North America", "What are the top 5 products by sales?", "Calculate total revenue by region"]

Response:"""
            )
            
            chain = LLMChain(llm=self.llm, prompt=example_queries_prompt)
            
            response = chain.run(
                schema_context=schema_context,
                count=count
            )
            
            # Clean and parse response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            # Try to parse as JSON array
            try:
                queries = json.loads(response)
                if isinstance(queries, list):
                    # Ensure we have the right number and they're strings
                    queries = [str(q).strip() for q in queries[:count] if q]
                    logger.info(f"Generated {len(queries)} example queries based on schema")
                    return {
                        'success': True,
                        'example_queries': queries
                    }
                else:
                    raise ValueError("Response is not a list")
            except (json.JSONDecodeError, ValueError) as e:
                # Fallback: try to extract queries from text
                logger.warning(f"Could not parse example queries as JSON: {str(e)}")
                # Try to extract quoted strings
                queries = re.findall(r'"([^"]+)"', response)
                if queries:
                    queries = queries[:count]
                    return {
                        'success': True,
                        'example_queries': queries
                    }
                else:
                    # Ultimate fallback: return generic queries
                    return {
                        'success': True,
                        'example_queries': [
                            'Show me all records from the first table',
                            'What are the top 5 items?',
                            'Calculate totals by category',
                            'Find records matching a condition',
                            'Show summary statistics'
                        ]
                    }
            
        except Exception as e:
            logger.error(f"Error generating example queries: {str(e)}")
            # Return fallback queries
            return {
                'success': True,
                'example_queries': [
                    'Show me all records from the first table',
                    'What are the top 5 items?',
                    'Calculate totals by category',
                    'Find records matching a condition',
                    'Show summary statistics'
                ]
            }


# Global RAG service instance
rag_service = RAGService()
