
# E-Commerce Order Analytics System using Python, Pandas, SQLite and SQL

**Celebal Technologies – Week 8 Mini Project**

## Project Overview

This project demonstrates the design and implementation of an end-to-end e-commerce analytics system using **Python**, **Pandas**, **SQLite**, and **SQL**. The workflow starts with generating realistic but intentionally imperfect datasets, followed by cleaning and validation, loading into a relational database, executing business analytics queries, and generating reports through a command-line interface.

The objective is not only to analyze sales data but also to simulate the type of data quality issues commonly encountered in production systems and resolve them before performing analytics.

---

# Objectives

- Generate realistic e-commerce datasets.
- Introduce controlled data quality issues.
- Clean and validate data using Pandas.
- Enforce relational integrity using SQLite.
- Perform analytical SQL queries using joins, aggregations,  CTEs, and window functions.
- Generate business reports from the command line.
- Validate edge cases to improve system reliability.

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Data generation and processing |
| Pandas | Data cleaning and validation |
| SQLite | Relational database |
| SQL | Business analytics |
| Faker | Synthetic dataset generation |
| Tabulate | CLI report formatting |

---

# Project Structure

```text
Week8-ecommerce_analytics_system/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── database/
│   └── ecommerce.db
│
├── docs/
│
├── output/
│   ├── reports/
│
├── scripts/
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── load_database.py
│   ├── report_cli.py
│   ├── run_queries.py
│   └── test_cases.py
│
├── sql/
│   ├── schema.sql
│   ├── basic_queries.sql
│   ├── advanced_queries.sql
│   └── cohort_analysis.sql
│
├── README.md
└── requirements.txt
```

---

# System Workflow

```text
Generate Raw Data
        │
        ▼
 Raw CSV Files
        │
        ▼
 Data Cleaning & Validation
        │
        ▼
 Clean CSV Files
        │
        ▼
 SQLite Database
        │
        ▼
 SQL Analytics
        │
        ▼
 CLI Reports
        │
        ▼
 Business Insights
```

---

# Dataset Description

## customers.csv

Stores customer profile information including customer type and registration details.

## products.csv

Contains product catalog information including category, subcategory, pricing, and ratings.

## orders.csv

Stores order-level information such as customer, order date, payment method, order status, and shipping details.

## order_items.csv

Contains product-level transaction details including quantity, price, and discounts.

---

# Intentional Data Quality Issues

To simulate real-world scenarios, the generated datasets include controlled inconsistencies such as:

- Missing customer IDs
- Invalid email addresses
- Duplicate records
- Mixed-case product names
- Extra whitespace
- Incorrect date formats
- Future order dates
- Invalid discounts (>100%)
- Negative quantities
- Broken foreign-key references

These issues are intentionally introduced and later resolved during the cleaning stage.

---

# Data Cleaning

The cleaning pipeline performs:

- Duplicate removal
- Whitespace trimming
- Product name normalization
- Email validation
- Date conversion
- Future date removal
- Negative shipping correction
- Quantity correction
- Discount validation
- Referential integrity checks

Cleaned datasets are exported to:

```text
data/cleaned/
```

---

# Database Design

The SQLite database contains four normalized tables:

- Customers
- Products
- Orders
- Order Items

Primary keys and foreign keys are used to maintain data relationships.

---

# SQL Analytics

The project implements a variety of SQL queries to generate business insights from transactional data.

## Basic Analytics

- Revenue by Product Category
- Monthly Revenue Trend
- Month-wise Order Count
- Top Selling Products
- Top Customers by Revenue
- Average Order Value (AOV)

## Intermediate Analytics

- Customers with No Delivered Orders
- Products with More Returns than Purchases
- Return Rate by Category

## Advanced Analytics

- Running Revenue Total
- Moving Average
- Customer Ranking using DENSE_RANK()
- Previous Month Comparison using LAG()
- Multi-Level CTE Analysis
- Customer Revenue Distribution
- First vs Last Purchased Category
- Year-over-Year Analysis

## Customer Analytics

- Cohort Retention Analysis
- Customer Segmentation
- RFM Analysis
- Spend Tier Classification
- Frequently Bought Together Products

---

# Command-Line Reports

# Command-Line Reporting Tool

The project includes an interactive command-line reporting tool that connects to the SQLite database and generates business reports for a selected time period.

Run:

```bash
python scripts/report_cli.py

---

# Edge Case Testing

The project validates several edge cases:

- Invalid order references
- Discounts greater than 100%
- Zero quantity
- Future orders

The tests are implemented in:

```text
scripts/test_cases.py
```

---

# How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate raw datasets:

```bash
python scripts/generate_data.py
```

Clean datasets:

```bash
python scripts/clean_data.py
```

Create database:

```bash
python scripts/load_database.py
```

Execute SQL queries:

```bash
python scripts/run_queries.py
```

Generate CLI reports:

```bash
python scripts/report_cli.py --report revenue
```

Run edge-case tests:

```bash
python scripts/test_cases.py
```

---

# Key Features

- End-to-end analytics workflow
- Automated data cleaning
- SQLite integration
- Modular Python scripts
- SQL analytics with window functions and CTEs
- Command-line reporting
- Edge-case validation
- Well-organized project structure

---

# Future Improvements

Possible future enhancements include:

- Interactive dashboard using Power BI or Streamlit
- MySQL/PostgreSQL support
- Automated ETL scheduling
- Logging and monitoring
- Unit testing with pytest
- Docker containerization
- Cloud deployment on Azure
- REST API for report generation



# Learning Outcomes

This project helped in understanding:

- Synthetic data generation using Faker
- Data preprocessing and validation using Pandas
- Relational database design using SQLite
- Writing analytical SQL queries with joins, CTEs and window functions
- Customer cohort and retention analysis
- Command-line application development in Python
- Data quality management and edge-case handling


# Conclusion

This project demonstrates the complete lifecycle of an analytics pipeline, from synthetic data generation to business reporting. It emphasizes data quality, relational database design, analytical SQL, and modular Python development. The implementation provides a practical foundation for understanding data engineering and analytics workflows in an e-commerce environment.
