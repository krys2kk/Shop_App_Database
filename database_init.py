import sqlite3

DB_FILE = "sklep.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        address TEXT
    );

    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
    );

    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    );
        
    CREATE TABLE IF NOT EXISTS order_details (
        detail_id INTEGER PRIMARY KEY NOT NULL,
        FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS inventory_movements (
        movement_id INTEGER PRIMARY KEY NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
        movement_type TEXT NOT NULL,
        quantity_change INTEGER NOT NULL,
        movement_date TEXT NOT NULL,
    );

    CREATE TABLE IF NOT EXISTS product_prices (
        price_id INTEGER PRIMARY KEY NOT NULL,
        FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE,
        price REAL NOT NULL,
        start_date TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()
    print("Baza danych została utworzona i jest gotowa do użycia.")

if __name__ == "__main__":
    init_db()