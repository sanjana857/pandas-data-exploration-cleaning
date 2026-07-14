"""
Purpose:
Generate realistic e-commerce datasets with intentional data quality issues.
These datasets will later be cleaned using Pandas and loaded into SQLite
for business analytics.
"""

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

# Configuration
fake = Faker("en_IN")

TOTAL_CUSTOMERS = 500
TOTAL_PRODUCTS = 300
TOTAL_ORDERS = 1000
TOTAL_ORDER_ITEMS = 2500

# Project folders

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = BASE_DIR / "data" / "raw"

RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

CUSTOMER_TYPES = [
    "REGULAR",
    "PREMIUM",
    "VIP"
]

ORDER_STATUS = [
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED"
]

PAYMENT_METHODS = [
    "UPI",
    "CARD",
    "COD",
    "NETBANKING"
]

REGIONS = [
    "North",
    "South",
    "East",
    "West"
]

CATEGORIES = {
    "Electronics": [
        "Mobile",
        "Laptop",
        "Accessories"
    ],
    "Fashion": [
        "Men",
        "Women",
        "Footwear"
    ],
    "Books": [
        "Fiction",
        "Education",
        "Comics"
    ],
    "Home": [
        "Furniture",
        "Kitchen",
        "Decor"
    ]
}

BRANDS = [
    "Samsung",
    "Apple",
    "Boat",
    "Nike",
    "Puma",
    "Sony",
    "Dell",
    "HP",
    "LG",
    "Lenovo"
]


# Helper Functions
def random_order_datetime():
    """
    Generate a random order date within the last 2 years.
    """

    start_date = datetime.now() - timedelta(days=730)
    end_date = datetime.now()

    random_seconds = random.randint(
        0,
        int((end_date - start_date).total_seconds())
    )

    return start_date + timedelta(seconds=random_seconds)

def generate_customers():
    # Generate customer master data with intentional inconsistencies.
    customers = []

    for customer_id in range(1, TOTAL_CUSTOMERS + 1):

        registration_date = fake.date_between(
            start_date="-3y",
            end_date="today"
        )

        email = fake.email()

        # Around 2% invalid emails
        if random.random() < 0.02:
            email = email.replace("@", "")

        customer = {
            "customer_id": customer_id,
            "customer_name": fake.name(),
            "email": email,
            "registration_date": registration_date,
            "customer_type": random.choice(CUSTOMER_TYPES),
            "city": fake.city(),
            "state": fake.state(),
            "region": random.choice(REGIONS)
        }

        customers.append(customer)

    df = pd.DataFrame(customers)

    # Introduce duplicate records
    duplicate_rows = df.sample(10)

    df = pd.concat(
        [df, duplicate_rows],
        ignore_index=True
    )

    df.to_csv(
        RAW_DATA_PATH / "customers.csv",
        index=False
    )

    print("customers.csv created")
    
    
def generate_products():
    """
    Generate product master data with realistic categories,
    pricing, and intentional formatting issues.
    """

    products = []

    for product_id in range(1, TOTAL_PRODUCTS + 1):

        category = random.choice(list(CATEGORIES.keys()))
        subcategory = random.choice(CATEGORIES[category])

        brand = random.choice(BRANDS)

        product_name = f"{brand} {subcategory}"

        # Cost price should always be lower
        cost_price = round(random.uniform(100, 3000), 2)

        selling_price = round(
            cost_price * random.uniform(1.10, 1.80),
            2
        )

        rating = round(
            random.uniform(3.0, 5.0),
            1
        )

        product = {
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "subcategory": subcategory,
            "brand": brand,
            "cost_price": cost_price,
            "selling_price": selling_price,
            "rating": rating
        }

        products.append(product)

    df = pd.DataFrame(products)
        # Add extra spaces to some product names
    random_rows = df.sample(frac=0.05).index

    df.loc[random_rows, "product_name"] = (
        "  " +
        df.loc[random_rows, "product_name"] +
        "   "
    )

    # Convert some names to lowercase
    random_rows = df.sample(frac=0.05).index

    df.loc[random_rows, "product_name"] = (
        df.loc[random_rows, "product_name"]
        .str.lower()
    )

    # Duplicate a few products
    duplicate_rows = df.sample(8)

    df = pd.concat(
        [df, duplicate_rows],
        ignore_index=True
    )

    df.to_csv(
        RAW_DATA_PATH / "products.csv",
        index=False
    )

    print("products.csv created")
    # Main Program
    
    

def generate_orders():
    
    """
    Generate order master data with realistic order history
    and intentional inconsistencies.
    """

    orders = []

    for order_id in range(1, TOTAL_ORDERS + 1):
        customer_id = random.randint(1,TOTAL_CUSTOMERS)
            
        if random.random() < 0.05:
            customer_id = None
            
        order_date = random_order_datetime()
        order_date = order_date.strftime("%Y-%m-%d %H:%M:%S")
        
        
        if random.random() < 0.03:

            dt = datetime.strptime(
                order_date,
                "%Y-%m-%d %H:%M:%S"
            )

            order_date = dt.strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        shipping_cost = round(random.uniform(40, 250), 2)
        order = {
            "order_id": order_id,

            "customer_id": customer_id,

            "order_date": order_date,

            "status": random.choice(ORDER_STATUS),

            "payment_method": random.choice(PAYMENT_METHODS),

            "shipping_cost": shipping_cost,

            "region": random.choice(REGIONS)
        }

        orders.append(order)
    df = pd.DataFrame(orders)
    duplicate_orders = df.sample(15)

    df = pd.concat(
        [df, duplicate_orders],
        ignore_index=True
    )
    future_rows = df.sample(frac=0.02).index

    future_date = (
        datetime.now() +
        timedelta(days=120)
    ).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    df.loc[
        future_rows,
        "order_date"
    ] = future_date

    shipping_rows = df.sample(frac=0.01).index

    df.loc[
        shipping_rows,
        "shipping_cost"
    ] = -50
    
    df.to_csv(
        RAW_DATA_PATH / "orders.csv",
        index=False
    )

    print("orders.csv created")
    
    
def generate_order_items():
    """
    Generate order items for every order.
    Each order can contain one or more products.
    """

    order_items = []
    item_id = 1
    TOTAL_ORDERS = 1000

    for order_id in range(1, TOTAL_ORDERS + 1):
        total_products = random.randint(1,5)
        for _ in range(total_products):
            product_id = random.randint(
                1,
                TOTAL_PRODUCTS
            )
            quantity = random.randint(1,5)
            if random.random() < 0.03:
                quantity = -quantity
            unit_price = round(
                random.uniform(200,5000),
                2
            )
            discount = round(
                random.uniform(0,50),
                2
            )
            if random.random() < 0.02:
                discount = 150
            row = {

                "item_id": item_id,

                "order_id": order_id,

                "product_id": product_id,

                "quantity": quantity,

                "unit_price": unit_price,

                "discount_percent": discount
            }
            order_items.append(row)

            item_id += 1
    df = pd.DataFrame(order_items)
    invalid_rows = df.sample(frac=0.01).index

    df.loc[
        invalid_rows,
        "order_id"
    ] = TOTAL_ORDERS + 500
    duplicates = df.sample(20)

    df = pd.concat(
        [df, duplicates],
        ignore_index=True
    )
    df.to_csv(
        RAW_DATA_PATH / "order_items.csv",
        index=False
    )

    print("order_items.csv created")
    
if __name__ == "__main__":

    print("Generating Raw E-Commerce Dataset")
    
    generate_customers()

    generate_products()

    generate_orders()

    generate_order_items()
    
    print("\nAll datasets generated successfully.")