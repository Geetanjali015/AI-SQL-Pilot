"""
Sample Database Generator
==========================
Creates a sample SQLite database with realistic e-commerce data for testing.
"""

import sqlite3
import random
from datetime import datetime, timedelta

def create_sample_database(db_path='sample_db.sqlite'):
    """Create sample database with e-commerce schema and data"""
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop existing tables if they exist
    cursor.execute('DROP TABLE IF EXISTS order_items')
    cursor.execute('DROP TABLE IF EXISTS orders')
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('DROP TABLE IF EXISTS categories')
    cursor.execute('DROP TABLE IF EXISTS customers')
    cursor.execute('DROP TABLE IF EXISTS regions')
    
    # Create tables
    
    # Regions table
    cursor.execute('''
        CREATE TABLE regions (
            region_id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_name VARCHAR(50) NOT NULL,
            country VARCHAR(50) NOT NULL
        )
    ''')
    
    # Customers table
    cursor.execute('''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20),
            region_id INTEGER,
            registration_date DATE NOT NULL,
            FOREIGN KEY (region_id) REFERENCES regions(region_id)
        )
    ''')
    
    # Categories table
    cursor.execute('''
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name VARCHAR(50) NOT NULL,
            description TEXT
        )
    ''')
    
    # Products table
    cursor.execute('''
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name VARCHAR(100) NOT NULL,
            category_id INTEGER,
            price DECIMAL(10, 2) NOT NULL,
            stock_quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    ''')
    
    # Orders table
    cursor.execute('''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            status VARCHAR(20) NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')
    
    # Order items table
    cursor.execute('''
        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')
    
    print("Tables created successfully")
    
    # Insert sample data
    
    # Regions
    regions = [
        ('North America', 'USA'),
        ('North America', 'Canada'),
        ('Europe', 'UK'),
        ('Europe', 'Germany'),
        ('Asia', 'Japan'),
        ('Asia', 'Singapore'),
        ('Australia', 'Australia')
    ]
    cursor.executemany('INSERT INTO regions (region_name, country) VALUES (?, ?)', regions)
    
    # Categories
    categories = [
        ('Electronics', 'Electronic devices and accessories'),
        ('Clothing', 'Fashion and apparel'),
        ('Books', 'Books and magazines'),
        ('Home & Garden', 'Home improvement and garden supplies'),
        ('Sports', 'Sports equipment and accessories'),
        ('Toys', 'Toys and games'),
        ('Food & Beverage', 'Food and drink products')
    ]
    cursor.executemany('INSERT INTO categories (category_name, description) VALUES (?, ?)', categories)
    
    # Customers
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa', 'James', 'Mary',
                   'William', 'Patricia', 'Richard', 'Jennifer', 'Charles', 'Linda', 'Thomas', 'Barbara']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez',
                  'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas']
    
    customers_data = []
    for i in range(100):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
        phone = f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        region_id = random.randint(1, 7)
        reg_date = (datetime.now() - timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d')
        customers_data.append((first_name, last_name, email, phone, region_id, reg_date))
    
    cursor.executemany('''
        INSERT INTO customers (first_name, last_name, email, phone, region_id, registration_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', customers_data)
    
    # Products
    products_data = [
        # Electronics
        ('Laptop Pro 15"', 1, 1299.99, 45),
        ('Wireless Mouse', 1, 29.99, 150),
        ('USB-C Hub', 1, 49.99, 200),
        ('Bluetooth Headphones', 1, 89.99, 75),
        ('Smartphone X', 1, 899.99, 30),
        ('Tablet 10"', 1, 399.99, 60),
        ('Smart Watch', 1, 299.99, 80),
        
        # Clothing
        ('Cotton T-Shirt', 2, 19.99, 300),
        ('Denim Jeans', 2, 49.99, 150),
        ('Winter Jacket', 2, 129.99, 50),
        ('Running Shoes', 2, 79.99, 100),
        ('Summer Dress', 2, 59.99, 80),
        
        # Books
        ('Python Programming Guide', 3, 39.99, 100),
        ('Data Science Handbook', 3, 49.99, 75),
        ('Fiction Novel Collection', 3, 24.99, 120),
        
        # Home & Garden
        ('Coffee Maker', 4, 79.99, 90),
        ('Vacuum Cleaner', 4, 199.99, 40),
        ('Garden Tool Set', 4, 89.99, 65),
        ('LED Lamp', 4, 34.99, 110),
        
        # Sports
        ('Yoga Mat', 5, 29.99, 150),
        ('Dumbbells Set', 5, 99.99, 70),
        ('Tennis Racket', 5, 119.99, 45),
        
        # Toys
        ('Building Blocks', 6, 39.99, 200),
        ('RC Car', 6, 69.99, 85),
        ('Board Game', 6, 29.99, 130)
    ]
    
    cursor.executemany('''
        INSERT INTO products (product_name, category_id, price, stock_quantity)
        VALUES (?, ?, ?, ?)
    ''', products_data)
    
    # Orders and Order Items
    statuses = ['completed', 'completed', 'completed', 'completed', 'processing', 'shipped', 'cancelled']
    
    order_id = 1
    for i in range(200):
        customer_id = random.randint(1, 100)
        order_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
        status = random.choice(statuses)
        
        # Generate 1-4 items per order
        num_items = random.randint(1, 4)
        order_total = 0
        order_items = []
        
        for j in range(num_items):
            product_id = random.randint(1, 25)
            quantity = random.randint(1, 3)
            
            # Get product price
            cursor.execute('SELECT price FROM products WHERE product_id = ?', (product_id,))
            unit_price = cursor.fetchone()[0]
            
            order_total += unit_price * quantity
            order_items.append((order_id, product_id, quantity, unit_price))
        
        # Insert order
        cursor.execute('''
            INSERT INTO orders (customer_id, order_date, total_amount, status)
            VALUES (?, ?, ?, ?)
        ''', (customer_id, order_date, order_total, status))
        
        # Insert order items
        cursor.executemany('''
            INSERT INTO order_items (order_id, product_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)
        ''', order_items)
        
        order_id += 1
    
    # Commit and close
    conn.commit()
    print(f"Sample database created successfully at {db_path}")
    print(f"- {len(regions)} regions")
    print(f"- {len(categories)} categories")
    print(f"- 100 customers")
    print(f"- {len(products_data)} products")
    print(f"- 200 orders with multiple items")
    
    conn.close()


if __name__ == '__main__':
    create_sample_database()
