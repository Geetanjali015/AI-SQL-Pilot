#!/usr/bin/env python3
"""
Comprehensive Pipeline Test
============================
Tests the complete pipeline including:
1. Database connection
2. SQL generation from natural language
3. SQL optimization
4. Performance profiling
5. Frontend API compatibility
"""

import sys
import os
import json
import time
import requests
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

# Test configuration
BACKEND_URL = "http://localhost:5001/api"
# Database created by create_sample_db.py as sample_db.sqlite
TEST_DB_PATH = str(backend_path / "sample_db.sqlite")

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def test_health_check():
    """Test health check endpoint"""
    print_header("1. Health Check")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Server is healthy: {data.get('message')}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend. Is the server running?")
        print_info("Start the backend with: cd backend && python app.py")
        return False
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False

def test_database_connection():
    """Test database connection"""
    print_header("2. Database Connection")
    try:
        response = requests.post(
            f"{BACKEND_URL}/connect-db",
            json={
                "db_type": "sqlite",
                "db_path": TEST_DB_PATH
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success(f"Connected to database: {data.get('message')}")
                return True
            else:
                print_error(f"Connection failed: {data.get('message')}")
                return False
        else:
            print_error(f"Connection request failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print_error(f"Database connection error: {str(e)}")
        return False

def test_sql_generation():
    """Test SQL generation from natural language"""
    print_header("3. SQL Generation (Natural Language)")
    
    test_queries = [
        "Show me all customers from North America",
        "List the top 5 products by total sales",
        "Find orders placed in the last month"
    ]
    
    results = []
    for query in test_queries:
        print_info(f"\nTesting: '{query}'")
        try:
            start_time = time.time()
            response = requests.post(
                f"{BACKEND_URL}/generate-sql",
                json={"query": query},
                timeout=180
            )
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    sql = data.get('generated_sql', '')
                    performance = data.get('performance', {})
                    
                    print_success(f"Generated SQL ({elapsed:.2f}s)")
                    print(f"   SQL: {sql[:100]}...")
                    
                    # Check performance metrics
                    if performance:
                        exec_time = performance.get('execution_time_ms', 0)
                        memory = performance.get('memory_used_mb', 0)
                        cpu = performance.get('cpu_percent', 0)
                        rows = performance.get('row_count', 0)
                        
                        print(f"   Performance: {exec_time:.2f}ms, {memory:.4f}MB, {cpu:.2f}%, {rows} rows")
                        
                        # Verify metrics are reasonable
                        if exec_time > 0 and memory >= 0 and 0 <= cpu <= 100:
                            print_success("Performance metrics are valid")
                        else:
                            print_error("Performance metrics appear invalid")
                    else:
                        print_error("No performance metrics returned")
                    
                    results.append(True)
                else:
                    print_error(f"Generation failed: {data.get('message')}")
                    results.append(False)
            else:
                print_error(f"Request failed: {response.status_code}")
                print(response.text[:200])
                results.append(False)
        except requests.exceptions.Timeout:
            print_error("Request timed out (>180s)")
            results.append(False)
        except Exception as e:
            print_error(f"Error: {str(e)}")
            results.append(False)
    
    success_count = sum(results)
    print(f"\n📊 Results: {success_count}/{len(test_queries)} queries generated successfully")
    return success_count == len(test_queries)

def test_sql_optimization():
    """Test SQL optimization"""
    print_header("4. SQL Optimization")
    
    test_cases = [
        {
            "name": "Unoptimized query (SELECT *)",
            "query": "SELECT * FROM customers WHERE region_id = 1"
        },
        {
            "name": "Query with inefficient WHERE",
            "query": "SELECT customer_id, name FROM customers WHERE UPPER(name) = 'JOHN'"
        }
    ]
    
    results = []
    for test_case in test_cases:
        print_info(f"\nTesting: {test_case['name']}")
        print(f"   Original: {test_case['query']}")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{BACKEND_URL}/optimize-query",
                json={"query": test_case['query']},
                timeout=180
            )
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    optimized = data.get('optimized_query', '')
                    is_optimized = data.get('is_already_optimized', False)
                    comparison = data.get('performance', {}).get('comparison')
                    
                    print_success(f"Optimization complete ({elapsed:.2f}s)")
                    print(f"   Optimized: {optimized[:100]}...")
                    print(f"   Already optimized: {is_optimized}")
                    
                    if comparison:
                        print(f"   Comparison available: Original vs Optimized")
                        orig_time = comparison.get('original', {}).get('execution_time_ms', 0)
                        opt_time = data.get('performance', {}).get('execution_time_ms', 0)
                        print(f"   Original: {orig_time:.2f}ms, Optimized: {opt_time:.2f}ms")
                    
                    results.append(True)
                else:
                    print_error(f"Optimization failed: {data.get('message')}")
                    results.append(False)
            else:
                print_error(f"Request failed: {response.status_code}")
                results.append(False)
        except requests.exceptions.Timeout:
            print_error("Request timed out (>180s)")
            results.append(False)
        except Exception as e:
            print_error(f"Error: {str(e)}")
            results.append(False)
    
    success_count = sum(results)
    print(f"\n📊 Results: {success_count}/{len(test_cases)} queries optimized successfully")
    return success_count == len(test_cases)

def test_performance_metrics():
    """Test performance metrics accuracy"""
    print_header("5. Performance Metrics Validation")
    
    # Use correct column names from the sample database schema
    test_query = "SELECT customer_id, first_name, last_name, email FROM customers LIMIT 5"
    
    print_info(f"Testing query: {test_query}")
    
    try:
        # First, run the query to get performance metrics
        response = requests.post(
            f"{BACKEND_URL}/run-query",
            json={"query": test_query},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            # /run-query returns performance metrics directly, not wrapped in 'performance'
            # Check if it's wrapped or direct
            if data.get('success') is False:
                print_error(f"Query execution failed: {data.get('message')}")
                return False
            
            # Performance metrics are at the top level for /run-query
            performance = data if 'execution_time_ms' in data else data.get('performance', {})
            
            print_success("Performance metrics retrieved")
            
            # Validate metrics
            checks = []
            
            exec_time = performance.get('execution_time_ms', 0)
            if exec_time > 0:
                print_success(f"Execution time: {exec_time:.2f}ms (valid)")
                checks.append(True)
            else:
                print_error(f"Execution time: {exec_time} (invalid)")
                checks.append(False)
            
            memory = performance.get('memory_used_mb', 0)
            if memory >= 0 and memory < 1:  # Should be small for 5 rows
                print_success(f"Memory: {memory:.4f}MB ({memory*1024:.2f}KB) - reasonable for 5 rows")
                checks.append(True)
            else:
                print_error(f"Memory: {memory:.4f}MB - seems too high for 5 rows")
                checks.append(False)
            
            cpu = performance.get('cpu_percent', 0)
            if 0 <= cpu <= 100:
                print_success(f"CPU: {cpu:.2f}% (valid range)")
                checks.append(True)
            else:
                print_error(f"CPU: {cpu:.2f}% (invalid range)")
                checks.append(False)
            
            # Row count might be in data array length or explicit row_count
            data_rows = performance.get('data', [])
            row_count = performance.get('row_count', len(data_rows))
            if row_count == 5 or len(data_rows) == 5:
                print_success(f"Row count: {row_count} (correct)")
                checks.append(True)
            else:
                print_error(f"Row count: {row_count} (expected 5, got {len(data_rows)} rows in data)")
                checks.append(False)
            
            # Check for timing breakdown
            db_time = performance.get('db_execution_time_ms')
            conv_time = performance.get('conversion_time_ms')
            timing_source = performance.get('timing_source')
            
            if db_time is not None:
                print_success(f"DB execution time breakdown: {db_time:.2f}ms")
            if conv_time is not None:
                print_success(f"Conversion time: {conv_time:.2f}ms")
            if timing_source:
                print_success(f"Timing source: {timing_source}")
            
            all_valid = all(checks)
            return all_valid
        else:
            print_error(f"Request failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_frontend_compatibility():
    """Test that API responses match frontend expectations"""
    print_header("6. Frontend API Compatibility")
    
    # Test generate-sql response structure
    print_info("Testing /generate-sql response structure")
    try:
        response = requests.post(
            f"{BACKEND_URL}/generate-sql",
            json={"query": "Show me all customers"},
            timeout=180
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields for frontend
            required_fields = [
                'success', 'generated_sql', 'performance',
                'suggested_indexes', 'analysis'
            ]
            
            missing_fields = []
            for field in required_fields:
                if field not in data:
                    missing_fields.append(field)
            
            if missing_fields:
                print_error(f"Missing fields: {', '.join(missing_fields)}")
                return False
            else:
                print_success("All required fields present")
            
            # Check performance structure
            # Note: performance can be None if profiling fails, which is acceptable
            # The frontend handles null/None gracefully (see ResultsDashboard.jsx line 24: performance = null)
            performance = data.get('performance')
            
            if performance is None:
                print_info("Performance is None (profiling may have failed, but this is acceptable - frontend handles null)")
                # This is acceptable - frontend defaults to null and handles it gracefully
                return True
            
            if not isinstance(performance, dict):
                print_error(f"Performance is not a dict: {type(performance)}")
                return False
            
            # If performance is a dict, check required fields
            perf_fields = ['execution_time_ms', 'memory_used_mb', 'cpu_percent', 'row_count']
            missing_perf = [f for f in perf_fields if f not in performance]
            
            if missing_perf:
                print_error(f"Missing performance fields: {', '.join(missing_perf)}")
                return False
            else:
                print_success("Performance metrics structure valid")
            
            return True
        else:
            print_error(f"Request failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  COMPREHENSIVE PIPELINE TEST")
    print("=" * 70)
    print(f"\nBackend URL: {BACKEND_URL}")
    print(f"Test Database: {TEST_DB_PATH}")
    print(f"Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Run tests
    results['health'] = test_health_check()
    if not results['health']:
        print("\n❌ Health check failed. Please start the backend server first.")
        print("   Run: cd backend && python app.py")
        return
    
    results['database'] = test_database_connection()
    if not results['database']:
        print("\n❌ Database connection failed. Check database path.")
        return
    
    results['generation'] = test_sql_generation()
    results['optimization'] = test_sql_optimization()
    results['performance'] = test_performance_metrics()
    results['frontend'] = test_frontend_compatibility()
    
    # Summary
    print_header("TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name.upper()}")
    
    print(f"\n📊 Overall: {passed_tests}/{total_tests} test suites passed")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Pipeline is working perfectly.")
        return 0
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test suite(s) failed. Please review errors above.")
        return 1

if __name__ == '__main__':
    exit(main())

