# test_profiler.py
import json
from models import db_connection
from services.sql_profiler import sql_profiler  # adjust path if your profiler file is elsewhere

# Short alias for cleaner usage
db = db_connection.db_connection

# Connect to a simple SQLite database for testing (no credentials required)
config = {
    "db_type": "sqlite",
    "db_path": "dev_test.db"
}
connect_result = db.connect(config)
print("Connection result:", connect_result)

try:
    # quick one-off in Python REPL or change test_profiler to:
    result = sql_profiler.profile_query("SELECT 1", runs=10, warmup=2)
    print(json.dumps(result, indent=2, default=str))
except Exception as e:
    print("Profiler test failed:", str(e))
finally:
    db.close()
