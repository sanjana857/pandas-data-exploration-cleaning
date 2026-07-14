"""
report_cli.py

Purpose:
Interactive command-line reporting tool for the
E-Commerce Order Analytics System.

"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from tabulate import tabulate

# Project Paths

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "database" / "ecommerce.db"

# Database Connection

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

# Helper Functions

def print_heading(title):
    """
    Display a formatted heading.
    """

    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)


def get_date(prompt):
    """
    Read and validate a date from user.
    """

    while True:

        user_input = input(prompt)

        try:

            return datetime.strptime(
                user_input,
                "%Y-%m-%d"
            )

        except ValueError:

            print("\nInvalid date format.")
            print("Please enter date as YYYY-MM-DD.\n")


def choose_report():

    print_heading("E-Commerce Analytics Report")

    print("1. Daily Report")

    print("2. Weekly Report")

    print("3. Monthly Report")

    while True:

        choice = input("\nEnter your choice (1-3): ")

        if choice in ["1", "2", "3"]:

            return choice

        print("Invalid choice. Please try again.")


def get_period(choice):

    if choice == "1":

        report_name = "Daily"

    elif choice == "2":

        report_name = "Weekly"

    else:

        report_name = "Monthly"

    print_heading(f"{report_name} Report")

    start_date = get_date("Enter Start Date (YYYY-MM-DD): ")

    end_date = get_date("Enter End Date   (YYYY-MM-DD): ")

    while end_date < start_date:

        print("\nEnd date cannot be before start date.\n")

        end_date = get_date(
            "Enter End Date (YYYY-MM-DD): "
        )

    return report_name, start_date, end_date


# Summary Report

def summary_report(start_date, end_date):
    """
    Display total orders, revenue and unique customers
    for the selected date range.
    """

    query = """
    SELECT

        COUNT(DISTINCT o.order_id),

        ROUND(

            SUM(

                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent / 100.0)

            ),

            2

        ),

        COUNT(DISTINCT o.customer_id)

    FROM orders o

    JOIN order_items oi

    ON o.order_id = oi.order_id

    WHERE DATE(o.order_date)

    BETWEEN ? AND ?;
    """

    cursor.execute(

        query,

        (

            start_date.strftime("%Y-%m-%d"),

            end_date.strftime("%Y-%m-%d")

        )

    )

    result = cursor.fetchone()

    total_orders = result[0] if result[0] else 0

    total_revenue = result[1] if result[1] else 0

    unique_customers = result[2] if result[2] else 0

    print_heading("Summary")

    print(f"Total Orders      : {total_orders}")

    print(f"Total Revenue     : ₹ {total_revenue}")

    print(f"Unique Customers  : {unique_customers}")
    
    
# Top Products

def top_products(start_date, end_date):
    """
    Display Top 3 selling products.
    """

    query = """
    SELECT

        p.product_name,

        SUM(oi.quantity) AS total_quantity,

        ROUND(

            SUM(

                oi.quantity *

                oi.unit_price *

                (1 - oi.discount_percent / 100.0)

            ),

            2

        ) revenue

    FROM products p

    JOIN order_items oi

    ON p.product_id = oi.product_id

    JOIN orders o

    ON oi.order_id = o.order_id

    WHERE DATE(o.order_date)

    BETWEEN ? AND ?

    GROUP BY p.product_name

    ORDER BY revenue DESC

    LIMIT 3;
    """

    cursor.execute(

        query,

        (

            start_date.strftime("%Y-%m-%d"),

            end_date.strftime("%Y-%m-%d")

        )

    )

    rows = cursor.fetchall()

    headers = [

        "Product",

        "Quantity",

        "Revenue"

    ]

    print_heading("Top 3 Products")

    if rows:

        print(

            tabulate(

                rows,

                headers=headers,

                tablefmt="grid"

            )

        )

    else:

        print("No records found.")
        

# Previous Period Comparison

def previous_period_report(start_date, end_date):
    """
    Compare current revenue with previous period.
    """

    days = (end_date - start_date).days + 1

    previous_end = start_date - timedelta(days=1)

    previous_start = previous_end - timedelta(days=days - 1)

    query = """
    SELECT

        ROUND(

            SUM(

                oi.quantity *

                oi.unit_price *

                (1 - oi.discount_percent / 100.0)

            ),

            2

        )

    FROM orders o

    JOIN order_items oi

    ON o.order_id = oi.order_id

    WHERE DATE(o.order_date)

    BETWEEN ? AND ?;
    """

    cursor.execute(

        query,

        (

            start_date.strftime("%Y-%m-%d"),

            end_date.strftime("%Y-%m-%d")

        )

    )

    current = cursor.fetchone()[0]

    cursor.execute(

        query,

        (

            previous_start.strftime("%Y-%m-%d"),

            previous_end.strftime("%Y-%m-%d")

        )

    )

    previous = cursor.fetchone()[0]

    current = current if current else 0

    previous = previous if previous else 0

    print_heading("Previous Period Comparison")

    print(f"Current Revenue   : ₹ {current}")

    print(f"Previous Revenue  : ₹ {previous}")

    if previous == 0:

        print("Growth            : N/A")

    else:

        growth = ((current - previous) / previous) * 100

        print(f"Growth            : {growth:.2f}%")
        

# Main Program


def main():
    """
    Main function to run the reporting tool.
    """

    # Select report type
    choice = choose_report()

    report_name, start_date, end_date = get_period(choice)

    print_heading(f"{report_name} Analytics Report")

    print(f"Report Period : {start_date.strftime('%Y-%m-%d')}  to  {end_date.strftime('%Y-%m-%d')}")

    # Display Summary
    summary_report(start_date, end_date)

    # Display Top Products
    top_products(start_date, end_date)

    # Compare with Previous Period
    previous_period_report(start_date, end_date)

    print("\n" + "=" * 70)
    print("Report Generated Successfully")
    print("=" * 70)



# Program Entry Point


if __name__ == "__main__":

    try:

        main()

    except sqlite3.Error as error:

        print("\nDatabase Error")

        print(error)

    except KeyboardInterrupt:

        print("\nProgram Interrupted.")

    finally:

        connection.close()
        