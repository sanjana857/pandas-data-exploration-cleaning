# RetailStream Inc. - End-to-End Data Engineering Pipeline

## Project Overview

RetailStream Inc. is an end-to-end Data Engineering project developed using **Databricks Community/Free Edition**. The project demonstrates how historical, incremental, streaming, and late-arriving retail data can be processed using modern Data Engineering concepts and organized through the **Medallion Architecture (Bronze → Silver → Gold)**.

The pipeline is built using **PySpark**, **Delta Lake**, **Spark SQL**, and **Databricks Auto Loader** to simulate a production-style retail data processing workflow.

---

## Objective

The objective of this project is to build a scalable data pipeline that can:

- Process historical batch data
- Handle incremental batch loads
- Ingest streaming data using Auto Loader
- Process late-arriving records using Delta MERGE
- Clean and enrich data for analytics
- Generate business-ready reports from the Gold Layer

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Databricks Free Edition | Development Environment |
| PySpark | Data Processing |
| Delta Lake | Storage Format |
| Spark SQL | Business Reporting |
| Databricks Auto Loader | Streaming Ingestion |
| Unity Catalog Volumes | Data Storage |
| Git & GitHub | Version Control |

---

## Project Architecture

The project follows the Medallion Architecture.

```
                 Source Files
                       │
      ┌────────────────┼────────────────┐
      │                │                │
 Historical      Incremental      Streaming
     Batch           Batch       (Auto Loader)
      │                │                │
      └────────────────┼────────────────┘
                       │
                Bronze Layer
                       │
                Silver Layer
                       │
                 Gold Layer
                       │
             Business Reports
```

---

## Project Workflow

The pipeline executes in the following sequence:

1. Historical Batch Load
2. Incremental Batch Load
3. Streaming Data Ingestion using Auto Loader
4. Late Arriving Data Processing using Delta MERGE
5. Silver Layer Data Cleaning & Enrichment
6. Gold Layer Business Report Generation

---

## Features Implemented

- Historical Batch Processing
- Incremental Data Loading
- Real-Time Streaming using Auto Loader
- Delta MERGE for Late Arriving Records
- Bronze-Silver-Gold Architecture
- Spark SQL Reports
- Parameterized Notebook using Widgets
- Reusable Helper Functions
- Logging
- Data Validation
- Modular Code Structure

---

## Project Folder Structure

```
RetailStream_Project/

│── RetailStream_Final_Project.ipynb
│── README.md
│── screenshots/
│
└── Databricks Unity Catalog
      │
      ├── data/
      │      ├── batch_initial/
      │      ├── batch_incremental/
      │      ├── late_arriving/
      │      ├── autoloader_landing/
      │      ├── customers.csv
      │      ├── products.csv
      │      └── stores.csv
      │
      ├── delta/
      │      ├── bronze/
      │      ├── silver/
      │      └── gold/
      │
      └── checkpoints/
```

---

## Bronze Layer

The Bronze Layer stores raw data collected from multiple ingestion sources.

Implemented components:

- Historical Batch Load
- Incremental Batch Load
- Streaming Transactions
- Late Arriving Data

---

## Silver Layer

The Silver Layer transforms raw data into cleaned and enriched datasets.

Operations performed:

- Data Cleaning
- Joins with Customer, Product and Store datasets
- Revenue Calculation
- Margin Calculation
- Data Validation

---

## Gold Layer

The Gold Layer generates analytical datasets for business reporting.

Reports generated:

- Monthly Sales Summary
- Sales by Category
- Sales by Region
- Top Products

---

## Validation

The notebook includes validation at multiple stages.

Examples include:

- Record Count Validation
- Duplicate Record Check
- Null Value Validation
- Schema Validation

---

## Logging

Simple logging functions are used throughout the notebook to improve readability and monitor execution.

The notebook logs:

- Pipeline Start
- Layer Completion
- Data Processing Steps
- Successful Execution

---

## Screenshots

Project execution screenshots are available inside the **screenshots/** folder.

The folder includes:

- Project Overview
- Workflow
- Bronze Layer
- Incremental Load
- Auto Loader
- Delta MERGE
- Silver Layer
- Gold Layer
- Pipeline Summary
- Databricks Folder Structure

---

## Important Note

**This project has been developed and executed entirely on Databricks Free Edition.**

All datasets, Delta tables, checkpoints, output files, and generated layers are stored and managed inside **Databricks Unity Catalog Volumes**.

Since the complete pipeline executes within Databricks, the generated Delta outputs are **not stored directly in this GitHub repository**. GitHub contains the notebook, documentation, and project screenshots, while the complete execution environment and generated outputs reside inside Databricks.

---

## Future Improvements

Possible future enhancements include:

- Power BI Dashboard Integration
- Databricks Job Scheduling
- CI/CD Pipeline
- Data Quality Monitoring
- Automated Alerts
- Cloud Deployment

---

## Repository Contents

- Notebook
- Documentation
- Project Screenshots
- GitHub Version History

---

## Author

Developed as part of the **Celebal Technologies Data Engineering Internship (Final Project)**.
