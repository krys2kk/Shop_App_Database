import backend as db
from datetime import datetime

class APIClient:
    @staticmethod
    def get_customers():
        return db.list_customers()
    
    @staticmethod
    def add_customer(name, email, phone, address):
        if not name or not email:
            raise ValueError("Nazwa i email są wymagane")
        if '@' not in email or '.' not in email:
            raise ValueError("Nieprawidłowy format emaila")
        if phone and not phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError("Nieprawidłowy format telefonu")
        
        db.add_customer(name, email, phone, address)
        return True

    @staticmethod
    def anonymize_customer(id):
        db.delete_customer_data(id)
        return True
    
    @staticmethod
    def delete_customer(id):
        history = db.get_customer_history(id)
        if history:
            raise ValueError("Nie można usunąć klienta który ma zamówienia.")
        db.delete_customer_completely(id)
        return True
    

    @staticmethod
    def get_products():
        return db.list_products()
    
    @staticmethod
    def add_product(name, desc):
        db.add_product(name, desc)
        return True
    
    @staticmethod
    def get_product_price(id):
        return db.get_product_price(id)
    
    @staticmethod
    def get_current_stock(id):
        return db.get_current_stock(id)
    
    @staticmethod
    def update_product_price(id, price, start_date = None):
        price = round(float(price), 2)
        if price <= 0:
            raise ValueError("Cena musi być większa od zera")
        if start_date is None:
            start_date = datetime.now()
        db.update_product_price(id, price, start_date)
        return True
    
    @staticmethod
    def add_inventory_movement(id, type, quantity, date = None):
        if date is None:
            date = datetime.now()
        db.add_inventory_movement(id, type, quantity, date)
        return True
    

    @staticmethod
    def add_order(c_id, status, date = None):
        if date is None:
            date = datetime.now()
        db.add_order(c_id, status, date)
        return True
    
    @staticmethod
    def add_order_item(o_id, p_id, quantity, unit_price):
        unit_price = round(float(unit_price), 2)
        db.add_order_details(o_id, p_id, quantity, unit_price)
        # Odejmij produkt z magazynu
        movement_date = datetime.now()
        db.add_inventory_movement(p_id, 'wydanie', -quantity, movement_date)
        return True
    
    @staticmethod
    def get_best_selling_products(limit=10):
        return db.get_best_selling_products(limit)
    
    @staticmethod
    def get_customer_history(c_id):
        return db.get_customer_history(c_id)
    
    @staticmethod
    def get_orders():
        orders = db.get_orders()
        return sorted(orders, key=lambda x: x['order_id'])
    
    @staticmethod
    def delete_order(order_id):
        db.delete_order(order_id)
        return True
    
    @staticmethod
    def get_order_details(order_id):
        return db.get_order_details(order_id)

    @staticmethod
    def list_inventory_movements(id):
        return db.list_inventory_movements(id)
    
    @staticmethod
    def update_order_status(order_id, status):
        db.update_order_status(order_id, status)
        return True

    @staticmethod
    def update_customer_info(id, name=None, email=None, phone=None, address=None):
        if email:
            if '@' not in email or '.' not in email:
                raise ValueError("Nieprawidłowy format emaila")
        if phone:
            if not phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
                raise ValueError("Nieprawidłowy format telefonu")
        
        db.update_customer_info(id, name, email, phone, address)
        return True

    @staticmethod
    def update_product(product_id, field, value):
        """Aktualizuje pole produktu (nazwa lub opis)"""
        if field == 'nazwa':
            db.update_product_name(product_id, value)
        elif field == 'opis':
            db.update_product_description(product_id, value)
        return True
    
    @staticmethod
    def check_inventory_on_order(products_to_order):
        db.check_inventory_on_order(products_to_order)
        return True

    @staticmethod
    def update_order_status(order_id, status):
        db.update_order_status(order_id, status)
        return True
    
    @staticmethod
    def list_inventory_movements(product_id):
        return db.list_inventory_movements(product_id)
    
    @staticmethod
    def create_full_order(customer_id, status, order_date, products):
        return db.create_full_order_transaction(customer_id, status, order_date, products)
    
    @staticmethod
    def get_database_file_path():
        return db.DB_FILE
    
    @staticmethod
    def get_price_history(product_id):
        return db.get_price_history(product_id)