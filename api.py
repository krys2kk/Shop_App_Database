from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
import backend as db
import database_init
import traceback

# Inicjalizacja bazy danych
database_init.init_db()

# Inicjalizacja Flask
app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

# ==================== CUSTOMERS ====================

@app.route('/api/customers', methods=['GET'])
def list_customers():
    """
    Pobiera listę wszystkich klientów
    ---
    responses:
      200:
        description: Lista klientów
    """
    try:
        customers = db.list_customers()
        return jsonify({"success": True, "data": customers}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/customers', methods=['POST'])
def create_customer():
    """
    Dodaje nowego klienta
    ---
    parameters:
      - in: body
        name: customer
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
            phone:
              type: string
            address:
              type: object
              properties:
                city:
                  type: string
                street:
                  type: string
                postal_code:
                  type: string
    responses:
      201:
        description: Klient został dodany
      400:
        description: Błąd danych
    """
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        address = data.get("address")

        if not name or not email:
            return jsonify({"success": False, "error": "Wymagane: name, email"}), 400

        result = db.add_customer(name, email, phone, address)
        return jsonify({"success": True, "message": result}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer_data(customer_id):
    """
    Usuwa lub anonimizuje klienta
    ---
    parameters:
      - in: path
        name: customer_id
        type: integer
    responses:
      200:
        description: Klient usunięty/anonimizowany
    """
    try:
        result = db.delete_customer_data(customer_id)
        return jsonify({"success": True, "message": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== PRODUCTS ====================

@app.route('/api/products', methods=['GET'])
def list_products():
    """
    Pobiera listę wszystkich produktów
    ---
    responses:
      200:
        description: Lista produktów
    """
    try:
        products = db.list_products()
        return jsonify({"success": True, "data": products}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/products', methods=['POST'])
def create_product():
    """
    Dodaje nowy produkt
    ---
    parameters:
      - in: body
        name: product
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
    responses:
      201:
        description: Produkt został dodany
    """
    try:
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")

        if not name or not description:
            return jsonify({"success": False, "error": "Wymagane: name, description"}), 400

        db.add_product(name, description)
        return jsonify({"success": True, "message": "Produkt dodany"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Aktualizuje produkt
    ---
    parameters:
      - in: path
        name: product_id
        type: integer
      - in: body
        name: product
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
    responses:
      200:
        description: Produkt zaktualizowany
    """
    try:
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")

        if not name or not description:
            return jsonify({"success": False, "error": "Wymagane: name, description"}), 400

        db.update_product(product_id, name, description)
        return jsonify({"success": True, "message": "Produkt zaktualizowany"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    Usuwa produkt
    ---
    parameters:
      - in: path
        name: product_id
        type: integer
    responses:
      200:
        description: Produkt usunięty
    """
    try:
        result = db.delete_product(product_id)
        return jsonify({"success": True, "message": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== PRICING ====================

@app.route('/api/products/<int:product_id>/price', methods=['POST'])
def set_product_price(product_id):
    """
    Ustawia nową cenę produktu
    ---
    parameters:
      - in: path
        name: product_id
        type: integer
      - in: body
        name: price_data
        schema:
          type: object
          properties:
            price:
              type: number
            start_date:
              type: string
    responses:
      201:
        description: Cena ustawiona
    """
    try:
        data = request.get_json()
        price = data.get("price")
        start_date = data.get("start_date")

        if price is None or not start_date:
            return jsonify({"success": False, "error": "Wymagane: price, start_date"}), 400

        db.update_product_price(product_id, price, start_date)
        return jsonify({"success": True, "message": "Cena ustawiona"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/products/<int:product_id>/current-price', methods=['GET'])
def get_product_price(product_id):
    """
    Pobiera aktualną cenę produktu
    ---
    parameters:
      - in: path
        name: product_id
        type: integer
    responses:
      200:
        description: Aktualna cena produktu
    """
    try:
        price = db.get_current_price(product_id)
        return jsonify({"success": True, "price": price}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== INVENTORY ====================

@app.route('/api/products/<int:product_id>/stock', methods=['GET'])
def get_stock(product_id):
    """
    Pobiera aktualny stan magazynu produktu
    ---
    parameters:
      - in: path
        name: product_id
        type: integer
    responses:
      200:
        description: Stan magazynu
    """
    try:
        stock = db.get_current_stock(product_id)
        return jsonify({"success": True, "stock": stock}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/products/<int:product_id>/stock-movement', methods=['POST'])
def add_stock_movement(product_id):
    """
    Dodaje ruch magazynowy (przychód, rozchód)
    ---
    parameters:
      - in: path
        name: product_id
        type: integer
      - in: body
        name: movement
        schema:
          type: object
          properties:
            movement_type:
              type: string
            quantity:
              type: integer
            movement_date:
              type: string
    responses:
      201:
        description: Ruch magazynowy dodany
    """
    try:
        data = request.get_json()
        movement_type = data.get("movement_type")
        quantity = data.get("quantity")
        movement_date = data.get("movement_date")

        if not movement_type or quantity is None or not movement_date:
            return jsonify({"success": False, "error": "Wymagane: movement_type, quantity, movement_date"}), 400

        db.add_inventory_movement(product_id, movement_type, quantity, movement_date)
        return jsonify({"success": True, "message": "Ruch magazynowy dodany"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== ORDERS ====================

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """
    Pobiera listę wszystkich zamówień
    ---
    responses:
      200:
        description: Lista zamówień
    """
    try:
        orders = db.get_orders()
        return jsonify({"success": True, "data": orders}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/orders', methods=['POST'])
def create_order():
    """
    Tworzy nowe zamówienie
    ---
    parameters:
      - in: body
        name: order
        schema:
          type: object
          properties:
            customer_id:
              type: integer
            status:
              type: string
            order_date:
              type: string
    responses:
      201:
        description: Zamówienie utworzone
    """
    try:
        data = request.get_json()
        customer_id = data.get("customer_id")
        status = data.get("status", "pending")
        order_date = data.get("order_date")

        if not customer_id or not order_date:
            return jsonify({"success": False, "error": "Wymagane: customer_id, order_date"}), 400

        order_id = db.add_order(customer_id, status, order_date)
        return jsonify({"success": True, "order_id": order_id}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """
    Aktualizuje status zamówienia
    ---
    parameters:
      - in: path
        name: order_id
        type: integer
      - in: body
        name: status
        schema:
          type: object
          properties:
            status:
              type: string
    responses:
      200:
        description: Status zaktualizowany
    """
    try:
        data = request.get_json()
        new_status = data.get("status")

        if not new_status:
            return jsonify({"success": False, "error": "Wymagane: status"}), 400

        db.update_order_status(order_id, new_status)
        return jsonify({"success": True, "message": "Status zaktualizowany"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/orders/<int:order_id>/items', methods=['POST'])
def add_order_item(order_id):
    """
    Dodaje pozycję do zamówienia
    ---
    parameters:
      - in: path
        name: order_id
        type: integer
      - in: body
        name: item
        schema:
          type: object
          properties:
            product_id:
              type: integer
            quantity:
              type: integer
            unit_price:
              type: number
    responses:
      201:
        description: Pozycja dodana do zamówienia
    """
    try:
        data = request.get_json()
        product_id = data.get("product_id")
        quantity = data.get("quantity")
        unit_price = data.get("unit_price")

        if not product_id or not quantity or unit_price is None:
            return jsonify({"success": False, "error": "Wymagane: product_id, quantity, unit_price"}), 400

        db.add_order_details(order_id, product_id, quantity, unit_price)
        return jsonify({"success": True, "message": "Pozycja dodana"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== ADVANCED REPORTS ====================

@app.route('/api/reports/best-selling-products', methods=['GET'])
def report_best_selling():
    """
    Pobiera najlepiej sprzedające się produkty (Raport zaawansowany #1)
    ---
    parameters:
      - in: query
        name: limit
        type: integer
        default: 10
    responses:
      200:
        description: Lista najlepiej sprzedających się produktów
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        products = db.get_best_selling_products(limit)
        return jsonify({"success": True, "data": products}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/reports/customer-history/<int:customer_id>', methods=['GET'])
def report_customer_history(customer_id):
    """
    Pobiera historię zamówień klienta (Raport zaawansowany #2)
    ---
    parameters:
      - in: path
        name: customer_id
        type: integer
    responses:
      200:
        description: Historia zamówień klienta
    """
    try:
        history = db.get_customer_history(customer_id)
        return jsonify({"success": True, "data": history}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/reports/orders-with-totals', methods=['GET'])
def report_orders_with_totals():
    """
    Pobiera zamówienia z sumami (Raport zaawansowany #3)
    ---
    parameters:
      - in: query
        name: limit
        type: integer
        default: 20
    responses:
      200:
        description: Lista zamówień z wartościami
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        orders = db.get_orders_with_total(limit)
        return jsonify({"success": True, "data": orders}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Sprawdza czy API działa
    ---
    responses:
      200:
        description: API działa poprawnie
    """
    return jsonify({"success": True, "message": "API is running"}), 200


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"success": False, "error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

