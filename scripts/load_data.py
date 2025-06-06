import json
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import time

def wait_for_postgres():
    max_retries = 30
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),  # Change to 'postgres' if running in Docker
                database=os.getenv('DB_NAME', 'scraped_data'),
                user=os.getenv('DB_USER', 'myuser'),
                password=os.getenv('DB_PASSWORD', 'mypassword')
            )
            conn.close()
            print("PostgreSQL is ready!")
            return True
        except psycopg2.OperationalError:
            print(f"Waiting for PostgreSQL... ({i+1}/{max_retries})")
            time.sleep(2)
    return False

def main():
    if not wait_for_postgres():
        print("Failed to connect to PostgreSQL")
        exit(1)
    
    # Connect to database
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'scraped_data'),
        user=os.getenv('DB_USER', 'myuser'),
        password=os.getenv('DB_PASSWORD', 'mypassword')
    )
    
    cursor = conn.cursor()
    
    # Create table matching your JSON structure
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT,
            brand TEXT,
            price DECIMAL(10,2),
            unit_price DECIMAL(10,2),
            unit_label TEXT,
            size TEXT,
            promo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Load JSON data
    with open('data/monoprix.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    # Insert data
    insert_query = """
        INSERT INTO products (name, brand, price, unit_price, unit_label, size, promo) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    inserted_count = 0
    for product in products:
        try:
            cursor.execute(insert_query, (
                product.get('name'),
                product.get('brand'),
                float(product.get('price', 0)) if product.get('price') else None,
                float(product.get('unit_price', 0)) if product.get('unit_price') else None,
                product.get('unit_label'),
                product.get('size'),
                product.get('promo')
            ))
            inserted_count += 1
        except Exception as e:
            print(f"Error inserting product {product.get('name', 'Unknown')}: {e}")
            continue
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"Successfully inserted {inserted_count} products into the database!")

if __name__ == "__main__":
    main()
