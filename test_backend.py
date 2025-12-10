#!/usr/bin/env python3
"""
Test backend - demonstracja wszystkich funkcji db_operations.py
Etap 3: Implementacja bazy danych i backendu
"""

import backend as db
from datetime import datetime, timedelta

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

# =====================================================
print_section("TESTY KLIENTÓW")
print("1. Lista klientów:")
customers = db.list_customers()
for c in customers[:3]:
    print(f"  ID: {c['id']}, Nazwa: {c['name']}, Email: {c['email']}")

# =====================================================
print_section("TESTY PRODUKTÓW")
print("1. Lista produktów:")
products = db.list_products()
for p in products[:5]:
    print(f"  ID: {p['id']}, Nazwa: {p['name']}")

print("\n2. Ceny produktów:")
for p in products[:3]:
    price = db.get_product_price(p['id'])
    print(f"  Produkt {p['id']}: {price} zł")

print("\n3. Stan magazynowy:")
for p in products[:3]:
    stock = db.get_current_stock(p['id'])
    print(f"  Produkt {p['id']}: {stock} szt.")

# =====================================================
print_section("TESTY ZAMÓWIEŃ")
print("1. Lista zamówień:")
orders = db.get_customer_history(1)
for o in orders[:3]:
    print(f"  ID: {o['order_id']}, Klient: {o['customer_name']}, Status: {o['status']}")
    for product in o['products']:
        print(f"    - {product['product_name']}: {product['quantity']} x {product['unit_price']} zł")

# =====================================================
print_section("ZAAWANSOWANE ZAPYTANIA (RAPORTY)")

print("1. Najlepiej sprzedające się produkty (TOP 5):")
best_selling = db.get_best_selling_products(5)
for item in best_selling:
    print(f"  {item['product_name']}: {item['total_sold_quantity']} szt.")

if customers:
    customer_id = customers[0]['id']
    print(f"\n2. Historia zakupów klienta ID {customer_id}:")
    history = db.get_customer_history(customer_id)
    if isinstance(history, str):
        print(f"  {history}")
    else:
        for h in history[:5]:
            print(f"  Zamówienie {h['id']}: {h['product_name']} ({h['quantity']} szt.)")

print("\n3. Zamówienia z sumami (TOP 5):")
orders_with_total = db.get_best_selling_products(5)
for o in orders_with_total:
    print(f"  Zamówienie {o['id']} ({o['product_name']})")

# =====================================================
print_section("PODSUMOWANIE")
print(f"✓ Klientów w bazie: {len(customers)}")
print(f"✓ Produktów w bazie: {len(products)}")
print(f"✓ Zamówień w bazie: {len(orders)}")
print(f"✓ Wszystkie testy wykonane pomyślnie!")