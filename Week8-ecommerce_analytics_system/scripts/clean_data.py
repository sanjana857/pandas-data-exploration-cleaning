"""

Purpose:
Read raw e-commerce datasets, clean data quality issues,
validate relationships between tables, and export cleaned datasets.

"""

from pathlib import Path
import pandas as pd

# Project Paths


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_PATH = BASE_DIR / "data" / "raw"

CLEAN_PATH = BASE_DIR / "data" / "cleaned"

REPORT_PATH = BASE_DIR / "output" / "reports"

CLEAN_PATH.mkdir(parents=True, exist_ok=True)

REPORT_PATH.mkdir(parents=True, exist_ok=True)

def load_data():
    """
    Load all raw datasets.
    """

    customers = pd.read_csv(RAW_PATH / "customers.csv")

    products = pd.read_csv(RAW_PATH / "products.csv")

    orders = pd.read_csv(RAW_PATH / "orders.csv")

    order_items = pd.read_csv(RAW_PATH / "order_items.csv")

    return customers, products, orders, order_items
    
def clean_customers(df):
    """
    Clean customer master data.
    """

    print("\nCleaning Customers...")

    original_rows = len(df)

    # Remove duplicate rows
    df = df.drop_duplicates()

    duplicates_removed = original_rows - len(df)

    # Remove extra spaces
    df["customer_name"] = df["customer_name"].str.strip()

    df["email"] = df["email"].str.strip()

    # Standardize customer type
    df["customer_type"] = df["customer_type"].str.upper()

    # Convert registration date
    df["registration_date"] = pd.to_datetime(
        df["registration_date"],
        errors="coerce"
    )

    # Remove future registration dates
    today = pd.Timestamp.today()

    future_dates = (df["registration_date"] > today).sum()

    df = df[df["registration_date"] <= today]

    print(f"Duplicates Removed : {duplicates_removed}")

    print(f"Future Dates Removed : {future_dates}")

    return df

def clean_products(df):

    """
    Clean product data.
    """

    print("\nCleaning Products...")

    original_rows = len(df)

    df = df.drop_duplicates()

    duplicates_removed = original_rows - len(df)

    # Remove spaces
    df["product_name"] = df["product_name"].str.strip()

    # Convert title case
    df["product_name"] = df["product_name"].str.title()

    # Remove negative prices

    df = df[df["cost_price"] > 0]

    df = df[df["selling_price"] > 0]

    print(f"Duplicates Removed : {duplicates_removed}")

    return df


def clean_orders(df):
    """
    Clean order data by fixing dates, removing duplicates,
    and validating important fields.
    """

    print("\nCleaning Orders...")

    original_rows = len(df)

    # Remove duplicate rows
    df = df.drop_duplicates()

    duplicates_removed = original_rows - len(df)

    # Convert order_date to datetime
    df["order_date"] = pd.to_datetime(
    df["order_date"],
    format="mixed",
    errors="coerce"
)

    # Remove invalid dates
    invalid_dates = df["order_date"].isna().sum()

    df = df.dropna(subset=["order_date"])

    # Remove future dates
    today = pd.Timestamp.now()

    future_orders = (df["order_date"] > today).sum()

    df = df[df["order_date"] <= today]

    # Shipping cost cannot be negative
    negative_shipping = (df["shipping_cost"] < 0).sum()

    df.loc[df["shipping_cost"] < 0, "shipping_cost"] = 0

    print(f"Duplicates Removed      : {duplicates_removed}")
    print(f"Invalid Dates Removed   : {invalid_dates}")
    print(f"Future Orders Removed   : {future_orders}")
    print(f"Negative Shipping Fixed : {negative_shipping}")

    return df


def clean_order_items(df):
    """
    Clean order item data.
    """

    print("\nCleaning Order Items...")

    original_rows = len(df)

    df = df.drop_duplicates()

    duplicates_removed = original_rows - len(df)

    # Remove zero quantity
    zero_quantity = (df["quantity"] == 0).sum()

    df = df[df["quantity"] != 0]

    # Convert negative quantity into positive
    negative_quantity = (df["quantity"] < 0).sum()

    df["quantity"] = df["quantity"].abs()

    # Fix discount >100
    invalid_discount = (df["discount_percent"] > 100).sum()

    df.loc[
        df["discount_percent"] > 100,
        "discount_percent"
    ] = 100

    print(f"Duplicates Removed : {duplicates_removed}")
    print(f"Zero Quantity      : {zero_quantity}")
    print(f"Negative Quantity  : {negative_quantity}")
    print(f"Invalid Discount   : {invalid_discount}")

    return df


def validate_emails(customers):
    """
    Find customers having invalid email addresses.
    """

    invalid = customers[
        ~customers["email"].str.contains("@", na=False)
    ]

    print(f"\nInvalid Emails : {len(invalid)}")

    return invalid


def check_referential_integrity(orders, order_items):
    """
    Check whether every order_item references
    a valid order.
    """

    invalid = order_items[
        ~order_items["order_id"].isin(
            orders["order_id"]
        )
    ]

    print(f"Broken Order References : {len(invalid)}")

    return invalid


def save_clean_data(customers,
                    products,
                    orders,
                    order_items):
    """
    Save cleaned datasets.
    """

    customers.to_csv(
        CLEAN_PATH / "customers_clean.csv",
        index=False
    )

    products.to_csv(
        CLEAN_PATH / "products_clean.csv",
        index=False
    )

    orders.to_csv(
        CLEAN_PATH / "orders_clean.csv",
        index=False
    )

    order_items.to_csv(
        CLEAN_PATH / "order_items_clean.csv",
        index=False
    )

    print("\nClean datasets saved.")
    

def create_issue_report(invalid_emails,
                        invalid_orders):
    """
    Generate a simple issue report.
    """

    report = REPORT_PATH / "issue_report.txt"

    with open(report, "w") as file:

        file.write("E-Commerce Data Cleaning Report\n")

        file.write("=" * 40 + "\n\n")

        file.write(
            f"Invalid Emails : {len(invalid_emails)}\n"
        )

        file.write(
            f"Broken Order References : {len(invalid_orders)}\n"
        )

    print("Issue report created.")



if __name__ == "__main__":

    customers, products, orders, order_items = load_data()

    customers = clean_customers(customers)

    products = clean_products(products)

    orders = clean_orders(orders)

    order_items = clean_order_items(order_items)

    invalid_emails = validate_emails(customers)

    invalid_orders = check_referential_integrity(
        orders,
        order_items
    )

    save_clean_data(
        customers,
        products,
        orders,
        order_items
    )

    create_issue_report(
        invalid_emails,
        invalid_orders
    )

    print("\nData Cleaning Completed Successfully.")