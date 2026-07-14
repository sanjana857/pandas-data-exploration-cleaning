"""
run_queries.py

Purpose:
Execute SQL queries stored in basic_queries.sql,
display the results in a formatted table,
and save the output to a report file.

"""

import sqlite3
from pathlib import Path
from tabulate import tabulate

# Project Paths

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "database" / "ecommerce.db"

SQL_FILE = BASE_DIR / "sql" / "basic_queries.sql"

REPORT_FILE = BASE_DIR / "output" / "reports" / "basic_query_results.txt"

# Connect to SQLite Database

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

# Read SQL Script

with open(SQL_FILE, "r", encoding="utf-8") as file:
    sql_script = file.read()

# Split SQL script into individual queries
queries = [
    query.strip()
    for query in sql_script.split(";")
    if query.strip()
]

# Open Report File

report = open(REPORT_FILE, "w", encoding="utf-8")

# print("=" * 70)
print("Executing SQL Queries")
# print("=" * 70)

report.write("E-Commerce Analytics Report\n")
report.write("=" * 70 + "\n\n")

# Execute Queries

for index, query in enumerate(queries, start=1):

    print(f"\nQUERY {index}")
    # print("-" * 70)

    report.write(f"\nQUERY {index}\n")
    report.write("-" * 70 + "\n")

    try:

        cursor.execute(query)

        rows = cursor.fetchall()

        if cursor.description is not None:

            column_names = [
                column[0]
                for column in cursor.description
            ]

            table = tabulate(
                rows,
                headers=column_names,
                tablefmt="grid"
            )

            print(table)

            report.write(table)
            report.write("\n\n")

        else:

            print("Query executed successfully.")

            report.write("Query executed successfully.\n\n")

    except Exception as error:

        print(f"Error: {error}")

        report.write(f"Error: {error}\n\n")

# Close Resources

report.close()

connection.close()

# print("\n" + "=" * 70)
print("All queries executed successfully.")
# print("=" * 70)

print(f"\nReport saved at:\n{REPORT_FILE}")