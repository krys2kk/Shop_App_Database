import sqlite3
from datetime import datetime

DB_file = "sklep.db"

def get_connection():
    return sqlite3.connect(DB_file)

def add_customer(name, email, phone, address):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO customers (name, email, phone, address)
    VALUES(?, ?, ?, ?)
    """, (name, email, phone, address))
    conn.commit()
    conn.close()
    print(f"Dodano klienta (name)")

def list_customers():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""SELECT * FROM customers""")
    results = [dict(row) for row in cur.fetchall()]
    conn.close()
    return results

def delete_customer_data(customer_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql_query = """        
        UPDATE customers
        SET
            name = 'klient anonimowy' || CAST (? AS TEXT),
            email = 'anonymous@client.com' || CAST (? AS TEXT),
            address = 'nieznany',
            phone = '0'
        WHERE 
            customer_id = ?;
        """
        cur.execute(sql_query, (customer_id))
        if cur.rowcount > 0:
            print(f"{customer_id} klient anonimowy")
        else:
            print(f"Brak kilenta o id {customer_id}")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()

def add_product(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO products (name) 
                   VALUES(?)""", (name))
    conn.commit()
    conn.close()
    print(f"Dodano przedmiot (name)")

def list_products():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""SELECT * FROM products""")
    results = [dict(row) for row in cur.fetchall()]
    conn.close()
    return results

def update_product_price(product_id, price, start_date):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql_query = """
        INSERT INTO product_prices (product_id, price, start_date)
            VALUES(?, ?, ?)
        """
        cur.execute(sql_query, (price, start_date, product_id))
        if cur.rowcount > 0:
            print(f"Cena produktu {product_id} została zaktualizowana")
        else:
            print(f"Brak produktu {product_id}")
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()

def add_inventory_movement(product_id, type, quantity, movement_date):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql_query = """
        INSERT INTO inventory_movements (product_id, movement_type, quantity_change, movement_date)
            VALUES(?, ?, ?, ?)
        """
        cur.execute(sql_query, (product_id, type, quantity, movement_date))
        if cur.rowcount > 0:
            print(f"Dodany został zapis zmiany produktu {product_id}")
        else:
            print(f"Brak produktu {product_id}")
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()

def list_inventory_movements():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""SELECT * FROM inventory_movements""")
    results = [dict(row) for row in cur.fetchall()]
    conn.close()
    return results

def add_order(customer_id, status, order_date):
    conn = get_connection()
    cur = conn.cursor()
    order_id = None # Zmienna do przechowania nowego ID

    try:
        # Prawidłowe zapytanie INSERT do tabeli 'orders'
        sql_query = """
        INSERT INTO orders (customer_id, status, order_date)
        VALUES (?, ?, ?)
        """
        
        # Wykonanie zapytania
        cur.execute(sql_query, (customer_id, status, order_date))
        
        # Kluczowe: Pobranie ID nowo wstawionego wiersza
        # Metoda lastrowid działa po pomyślnym wykonaniu INSERT
        order_id = cur.lastrowid
        
        conn.commit()
        
        print(f"Dodano nagłówek zamówienia (order_id: {order_id})")
        
        # Zwracamy ID, aby użyć go w kolejnej funkcji (add_order_details)
        return order_id 

    except sqlite3.Error as e:
        print(f"Błąd SQLite podczas dodawania zamówienia: {e}")
        conn.rollback()
        return None
        
    finally:
        conn.close()

def add_order_details(order_id, product_id, quantity, unit_price):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql_query = """
        INSERT INTO order_details (order_id, product_id, quantity, unit_price)
            VALUES(?, ?, ?, ?)
        """
        cur.execute(sql_query, (order_id, product_id, quantity, unit_price))
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()

def update_product_price(product_id, price, start_date):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql_query = """
        INSERT INTO product_prices (product_id, price, start_date)
            VALUES(?, ?, ?)
        """
        cur.execute(sql_query, (product_id, price, start_date))
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()