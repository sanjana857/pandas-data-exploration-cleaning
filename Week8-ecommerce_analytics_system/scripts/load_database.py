"""
load_database.py

Purpose:
Create SQLite database from cleaned CSV files.
"""

import sqlite3
from pathlib import Path
import pandas as pd

# Project Paths

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "database" / "ecommerce.db"

SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"

CLEAN_DATA_PATH = BASE_DIR / "data" / "cleaned"

# Create Database

def create_database():

    print("Creating SQLite Database")

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    with open(SCHEMA_PATH, "r") as file:
        schema = file.read()

    cursor.executescript(schema)

    connection.commit()

    print("Database schema created successfully.")

    return connection

def load_csv_files(connection):
    """
    Load cleaned CSV files into SQLite tables.
    """

    customers = pd.read_csv(CLEAN_DATA_PATH / "customers_clean.csv")

    products = pd.read_csv(CLEAN_DATA_PATH / "products_clean.csv")

    orders = pd.read_csv(CLEAN_DATA_PATH / "orders_clean.csv")

    order_items = pd.read_csv(CLEAN_DATA_PATH / "order_items_clean.csv")

    customers.to_sql(
        "customers",
        connection,
        if_exists="append",
        index=False
    )

    products.to_sql(
        "products",
        connection,
        if_exists="append",
        index=False
    )

    orders.to_sql(
        "orders",
        connection,
        if_exists="append",
        index=False
    )

    order_items.to_sql(
        "order_items",
        connection,
        if_exists="append",
        index=False
    )

    print("\nData Loaded Successfully")

    print(f"Customers   : {len(customers)}")

    print(f"Products    : {len(products)}")

    print(f"Orders      : {len(orders)}")

    print(f"Order Items : {len(order_items)}")
    
    
def verify_database(connection):
    """
    Verify inserted row counts.
    """

    print("\nDatabase Verification")

    tables = [
        "customers",
        "products",
        "orders",
        "order_items"
    ]

    cursor = connection.cursor()

    for table in tables:

        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        total = cursor.fetchone()[0]

        print(f"{table:<15} {total}")
        

def close_database(connection):

    connection.close()

    print("\nDatabase connection closed.")
    
    
if __name__ == "__main__":

    connection = create_database()

    load_csv_files(connection)

    verify_database(connection)

    close_database(connection)

    print("\nSQLite database created successfully.")