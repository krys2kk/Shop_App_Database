from faker import Faker
import backend as db
from datetime import datetime, timedelta
import random

fake = Faker('pl_PL')
def seed_database():
    for i in range(10):
        db.add_customer(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address()
        )
    
    product_names=["Laptop Lenovo", "Monitor Dell", "Klawiatura SPC", "Myszka LogiTech", "Słuchawki SteelSeries",
                   "Płyta Główna MSI", "StreamDeck", "Mikrofon Razer", "Dysk SSD Samsung", "Karta Graficzna Nvidia"]
    for name in product_names:
        db.add_product(name=name, description=fake.sentence())
    
    for p_id in range(1,11):
        db.add_inventory_movement(
            product_id=p_id,
            type="dostawa",
            quantity=random.randint(10, 100),
            movement_date=datetime.now().date()
        )
    order_statuses=["oczekuje na płatność", "opłacone", "dostarczone", "anulowane"]
    for customer_id in range (1, 11):
        order_date=datetime.now()-timedelta(days=random.randint(1, 30))
        order_id=db.add_order(
            customer_id=customer_id,
            status=random.choice(order_statuses),
            order_date=order_date.date()
        )

        num_products = random.randint(2, 5)
        for _ in range(num_products):
            product_id=random.randint(1, 10)
            quantity=random.randint(1, 5)
            price=round(random.uniform(50, 2000), 10)
            db.add_order_details(order_id, product_id, quantity, price)
            db.add_inventory_movement( 
                product_id=p_id,
                type="rozchód",
                quantity=-quantity,
                movement_date=datetime.now().date()
            )
if __name__ == "__main__":
    seed_database()