# Week 7 - Delta Lake Assignment

## Objective

The objective of this assignment is to perform incremental data processing using Delta Lake using the Superstore dataset. The assignment demonstrates data loading, cleaning, Delta table creation, incremental data simulation, MERGE operations, and result validation.

---

## Technologies Used

- Databricks Free Edition
- Apache Spark (PySpark)
- Delta Lake
- Git & GitHub

---

## Dataset

- **Dataset:** Sample Superstore Dataset
- **Source:** Kaggle
- **Records:** 9,994
- **Columns:** 21

---

## Steps Performed

1. Loaded the Superstore dataset into Databricks.
2. Explored the dataset by checking the schema, row count, and null values.
3. Removed duplicate records.
4. Renamed column names to make them Delta-compatible.
5. Created a Delta table.
6. Simulated incremental data by:
   - Updating existing records.
   - Adding a new customer record.
7. Applied the MERGE operation to update and insert records.
8. Validated the final dataset by checking row counts and duplicate records.

---

## Key Learnings

- Learned how Delta Lake supports ACID transactions.
- Understood the MERGE operation for handling updates and inserts.
- Learned the importance of data cleaning before storing data in Delta tables.
- Performed validation to ensure data consistency after incremental processing.

---

## Challenges Faced

- Delta table creation initially failed because column names contained spaces.
- Resolved the issue by replacing spaces with underscores.
- Learned how Delta Lake handles incremental updates efficiently using the MERGE operation.

---

## Conclusion

This assignment provided hands-on experience with Delta Lake and incremental data processing using Apache Spark. It demonstrated how updates and new records can be managed efficiently while maintaining data consistency.