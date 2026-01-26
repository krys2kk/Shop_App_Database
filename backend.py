import os
import sys
import sqlite3
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sklep.db')

def get_connection():
    return sqlite3.connect(DB_FILE)

def add_customer(name, email, phone, address):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO customers (name, email, phone, address)
    VALUES(?, ?, ?, ?)
    """, (name, email, phone, address))
    conn.commit()
    conn.close()
    print(f"Dodano klienta {name}")

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
            phone = '000000000'
        WHERE 
            id = ?;
        """
        cur.execute(sql_query, (customer_id, customer_id, customer_id))
        if cur.rowcount > 0:
            print(f"Klient o id {customer_id} anonimizowany")
        else:
            print(f"Brak klienta o id {customer_id}")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()

def delete_customer_completely(customer_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        if cur.rowcount > 0:
            print(f"Klient o id {customer_id} całkowicie usunięty")
        else:
            print(f"Brak klienta o id {customer_id}")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()

def add_product(name, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO products (name, description) 
                   VALUES(?, ?)""", (name, description))
    conn.commit()
    conn.close()
    print(f"Dodano przedmiot {name}")

def list_products():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""SELECT * FROM products""")
    results = [dict(row) for row in cur.fetchall()]
    conn.close()
    return results

def add_inventory_movement(product_id, type, quantity, movement_date):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql_query = """
        INSERT INTO inventory_movements (product_id, movement_type, quantity_change, movement_date)
            VALUES(?, ?, ?, ?)
        """
        cur.execute(sql_query, (product_id, type, quantity, movement_date))
        conn.commit()
        if cur.rowcount > 0:
            print(f"Dodany został zapis zmiany produktu {product_id}")
        else:
            print(f"Brak produktu {product_id}")
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()

def list_inventory_movements(p_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""SELECT * FROM inventory_movements WHERE product_id = ?""", (p_id,))
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
        conn.commit()
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()

def update_product_price(product_id, price, start_date):
    conn = get_connection()
    cur = conn.cursor()
    if isinstance(start_date, datetime):
        formatted_date = start_date.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(start_date, str):
        formatted_date = start_date
    else:
        print("Błąd: Data musi być obiektem datetime lub string.")
    try:
        sql_query = """
            INSERT INTO product_prices (product_id, price, start_date)
            VALUES(?, ?, ?)
        """
        cur.execute(sql_query, (product_id, price, formatted_date))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()

def update_order_status(order_id, status):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql_query = """ 
        UPDATE orders
        SET status = ?
        WHERE id = ?;
        """
        cur.execute(sql_query, (status, order_id))
        conn.commit()
        if cur.rowcount > 0:
            print(f"Status zamówienia {order_id} zaktualizowany.")
        else:
            print(f"Brak zamówienia o id {order_id}")
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()

def update_customer_info(c_id, c_name, c_email, c_phone, c_address):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql_query = """
        UPDATE customers
        SET
            name = ?,
            email = ?,
            phone = ?,
            address = ?
        WHERE
            id = ?;
        """
        cur.execute(sql_query, (c_name, c_email, c_phone, c_address, c_id))
        conn.commit()
        if cur.rowcount > 0:
            print(f"Dane klienta {c_id} zaktualizowane.")
        else:
            print(f"Brak klienta o id {c_id}")
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()

def update_product_description(p_id, description):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE products SET description = ? WHERE id = ?", (description, p_id))
        conn.commit()
        print(f"Opis produktu {p_id} zaktualizowany")
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()

def update_product_name(p_id, name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE products SET name = ? WHERE id = ?", (name, p_id))
        conn.commit()
        print(f"Nazwa produktu {p_id} zaktualizowana na: {name}")
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_product_price(p_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql_query = """
        SELECT price
        FROM product_prices
        WHERE product_id = ? AND start_date <= ?
        ORDER BY start_date DESC
        LIMIT 1;
        """
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(sql_query, (p_id, current_date,))
        result = cur.fetchone()
        if result and result[0] is not None:
            return round(float(result[0]), 2)
        else:
            return None
    except sqlite3.Error as e:
        print(f"Błąd SQLite {e}")
        return None
    finally:
        conn.close()

def get_current_stock(p_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql_query = """
        SELECT
            SUM(quantity_change) AS cur_stock
        FROM
            inventory_movements
        WHERE
            product_id = ?;
        """
        cur.execute(sql_query, (p_id,))
        result = cur.fetchone()
        if result and result[0] is not None:
            return int(result[0])
        else:
            return 0
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        return -1
    finally:
        conn.close()

def get_best_selling_products(limit=10):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        sql_query = """
        SELECT
            p.id,
            p.name AS product_name,
            SUM(od.quantity) AS total_sold_quantity
        FROM
            products p
        INNER JOIN
            order_details od ON p.id = od.product_id
        GROUP BY
            product_name, p.name
        ORDER BY
            total_sold_quantity DESC
        LIMIT ?;
        """
        cur.execute(sql_query, (limit,))
        results = [dict(row) for row in cur.fetchall()]
        return results
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        return []
    finally:
        conn.close()

def get_customer_history(c_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        sql_query = """
        SELECT
            o.id AS order_id,
            o.order_date,
            o.status,
            od.product_id,
            od.quantity,
            od.unit_price,
            p.name AS product_name
        FROM
            orders o
        INNER JOIN
            order_details od ON o.id = od.order_id
        INNER JOIN
            products p ON od.product_id = p.id
        WHERE
            o.customer_id = ?
        ORDER BY
            o.order_date DESC, o.id DESC;
        """
        cur.execute(sql_query, (c_id,))
        results = [dict(row) for row in cur.fetchall()]
        if not results:
            print(f"Nie znaleziono klienta {c_id}")
        return results
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        return []
    finally:
        conn.close()

def check_inventory_on_order(products_to_order):
    unavailable_products = []
    for product_id, desired_quantity, unit_price  in products_to_order:
        current_stock = get_current_stock(product_id)
        if desired_quantity > current_stock:
            unavailable_products.append({
                'product_id': product_id,
                'available': current_stock,
                'required': desired_quantity
            })
    if unavailable_products:
        print("Niektóre produkty są niedostępne w wystarczającej ilości.")
        return False, unavailable_products
    else:
        print("Wszystkie produkty są dostępne.")
        return True, []

def create_full_order_transaction(customer_id, status, order_date, products_list):
    conn = get_connection()
    cur = conn.cursor()
    try:
        is_available, _ = check_inventory_on_order(products_list)
        if not is_available:
            raise ValueError("Brak towaru na magazynie. Transakcja anulowana.")
        cur.execute("INSERT INTO orders (customer_id, status, order_date) VALUES (?, ?, ?)", (customer_id, status, order_date))
        order_id = cur.lastrowid

        for product_id, quantity, unit_price in products_list:
            cur.execute("INSERT INTO order_details (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)", (order_id, product_id, quantity, unit_price))
            movement_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            quantity_change = -quantity
            cur.execute("INSERT INTO inventory_movements (product_id, movement_type, quantity_change, movement_date) VALUES (?, ?, ?, ?)", (product_id, 'wydanie', quantity_change, movement_date))
        conn.commit()
        print(f"Pomyślnie utworzono zamówienie {order_id} i zaktualizowano stany magazynowe.")
        return order_id
    except sqlite3.Error as e:
        print(f"Błąd transakcji: {e}. Wycofuję zmiany.")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_orders():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        sql_query = """
        SELECT
            o.id AS order_id,
            o.customer_id,
            c.name AS customer_name,
            o.order_date,
            o.status
        FROM
            orders o
        INNER JOIN
            customers c ON o.customer_id = c.id
        ORDER BY
            o.id ASC;
        """
        cur.execute(sql_query)
        results = [dict(row) for row in cur.fetchall()]
        return results
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        return []
    finally:
        conn.close()

def delete_order(order_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # First delete order details
        cur.execute("DELETE FROM order_details WHERE order_id = ?", (order_id,))
        # Then delete the order
        cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
        print(f"Usunięto zamówienie {order_id}")
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_order_details(order_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        sql_query = """
        SELECT
            od.product_id,
            p.name AS product_name,
            od.quantity,
            od.unit_price,
            (od.quantity * od.unit_price) AS total_price
        FROM
            order_details od
        INNER JOIN
            products p ON od.product_id = p.id
        WHERE
            od.order_id = ?
        ORDER BY
            od.product_id ASC;
        """
        cur.execute(sql_query, (order_id,))
        results = [dict(row) for row in cur.fetchall()]
        return results
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        return []
    finally:
        conn.close()

def get_price_history(product_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        sql_query = """
        SELECT
            price,
            start_date
        FROM
            product_prices
        WHERE
            product_id = ?
        ORDER BY
            start_date DESC;
        """
        cur.execute(sql_query, (product_id,))
        results = [dict(row) for row in cur.fetchall()]
        return results
    except sqlite3.Error as e:
        print(f"Błąd SQLite: {e}")
        return []
    finally:
        conn.close()