import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:5001/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 120 seconds (2 minutes) for LLM operations
});

// Add request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.message);
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// API methods
export const connectDatabase = async (dbConfig) => {
  const response = await api.post('/connect-db', dbConfig);
  return response.data;
};

export const disconnectDatabase = async () => {
  const response = await api.post('/disconnect-db');
  return response.data;
};

export const getSchema = async () => {
  const response = await api.get('/get-schema');
  return response.data;
};

export const generateSQL = async (naturalQuery) => {
  // Use longer timeout for LLM operations
  const response = await api.post('/generate-sql', { query: naturalQuery }, {
    timeout: 180000 // 3 minutes for SQL generation
  });
  return response.data;
};

export const runQuery = async (sqlQuery) => {
  const response = await api.post('/run-query', { query: sqlQuery });
  return response.data;
};

export const compareQueries = async (originalQuery, optimizedQuery) => {
  const response = await api.post('/compare-queries', {
    original_query: originalQuery,
    optimized_query: optimizedQuery,
  });
  return response.data;
};

export const optimizeQuery = async (query) => {
  // Use longer timeout for LLM operations
  const response = await api.post('/optimize-query', { query }, {
    timeout: 180000 // 3 minutes for query optimization
  });
  return response.data;
};

export const analyzeQuery = async (query) => {
  const response = await api.post('/analyze-query', { query });
  return response.data;
};

export const getSuggestions = async (query) => {
  const response = await api.post('/get-suggestions', { query });
  return response.data;
};

export const getSystemMetrics = async () => {
  const response = await api.get('/system-metrics');
  return response.data;
};

export const generateExampleQueries = async (count = 5) => {
  const response = await api.get('/generate-example-queries', {
    params: { count }
  });
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
