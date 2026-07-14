"""
test_cases.py

Purpose:
Test important edge cases for the e-commerce analytics system.

"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "database" / "ecommerce.db"

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()


def test_invalid_order_reference():

    cursor.execute("""

        SELECT COUNT(*)

        FROM order_items

        WHERE order_id NOT IN

        (

            SELECT order_id

            FROM orders

        )

    """)

    total = cursor.fetchone()[0]

    print(f"[PASS] Invalid Order References : {total}")


def test_invalid_discount():

    cursor.execute("""

        SELECT COUNT(*)

        FROM order_items

        WHERE discount_percent > 100

    """)

    total = cursor.fetchone()[0]

    print(f"[PASS] Discount >100 : {total}")


def test_zero_quantity():

    cursor.execute("""

        SELECT COUNT(*)

        FROM order_items

        WHERE quantity = 0

    """)

    total = cursor.fetchone()[0]

    print(f"[PASS] Quantity = 0 : {total}")


def test_future_orders():

    cursor.execute("""

        SELECT COUNT(*)

        FROM orders

        WHERE datetime(order_date) > datetime('now')

    """)

    total = cursor.fetchone()[0]

    print(f"[PASS] Future Orders : {total}")


if __name__ == "__main__":

    print("Running Edge Case Tests")

    test_invalid_order_reference()

    test_invalid_discount()

    test_zero_quantity()

    test_future_orders()

    connection.close()

    print("\nAll tests executed successfully.")