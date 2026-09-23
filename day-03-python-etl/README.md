Day 3 - Python ETL Pipeline
Overview

Day 3 evolves the Day 2 data-cleaning script into a reusable Python ETL pipeline.

The pipeline follows a standard:

Extract -> Transform -> Validate -> Load


architecture.

Raw CSV
   |
   v
EXTRACT
   |
   v
TRANSFORM
   |
   v
VALIDATE
   |
   v
LOAD
   |
   v
Processed CSV
   |
   v
PostgreSQL


The pipeline is designed to be rerunnable, use project-relative paths, preserve the original raw dataset, validate business rules, maintain the Day 1 revenue calculation, and produce logging and an ETL run report.

Day 3 Objective

The objective of Day 3 is to understand how a one-time data-cleaning script can be converted into a structured ETL pipeline.

The pipeline separates responsibilities into different stages:

Extract data from the raw CSV.

Transform and clean the data.

Validate the transformed dataset.

Load the processed dataset.

Generate an ETL execution report.

Record pipeline activity in a log file.

Handle failures clearly.

What Is ETL?

ETL stands for:

Extract -> Transform -> Load

Extract

Extract means reading data from a source.

In this project, the source is:

data/raw/ecommerce.csv


The pipeline reads the CSV using Pandas.

Transform

Transform means cleaning and changing the source data into the required format.

The transformation stage:

Standardizes column names.

Converts data types.

Standardizes text values.

Validates missing values.

Checks duplicate records.

Validates business rules.

Creates financial columns.

Calculates gross amount.

Calculates discount amount.

Calculates net amount.

Reconciles business revenue.

Validate

Validation verifies that the transformed data satisfies expected quality and business rules.

The pipeline checks:

Required columns.

Row count.

Missing values.

Duplicate order IDs.

ID values.

Quantity.

Unit price.

Discount.

Dates.

Financial calculations.

Business revenue.

Load

Load means writing the validated transformed data to the destination.

For Day 3, the destination is:

data/processed/ecommerce_clean.csv

Why ETL Is Different From a One-Off Cleaning Script

A one-off cleaning script is usually designed to solve a single immediate task.

An ETL pipeline is designed to be:

Repeatable.

Structured.

Reusable.

Validated.

Observable.

Easier to maintain.

Easier to automate later.

Day 2 focused mainly on cleaning the dataset.

Day 3 organizes that logic into a pipeline with separate Extract, Transform, Validate, and Load responsibilities.

Day 3 Architecture
                     +---------------------+
                     |   Raw CSV Dataset   |
                     |   ecommerce.csv     |
                     +----------+----------+
                                |
                                v
                     +---------------------+
                     |       EXTRACT       |
                     |      extract.py     |
                     +----------+----------+
                                |
                                v
                     +---------------------+
                     |      TRANSFORM      |
                     |     transform.py    |
                     +----------+----------+
                                |
                                v
                     +---------------------+
                     |      VALIDATE       |
                     |     validate.py     |
                     +----------+----------+
                                |
                                v
                     +---------------------+
                     |        LOAD         |
                     |       load.py       |
                     +----------+----------+
                                |
                                v
                     +---------------------+
                     |   Processed CSV     |
                     | ecommerce_clean.csv |
                     +----------+----------+
                                |
                                v
                     +---------------------+
                     |     PostgreSQL      |
                     |    ecommerce_db     |
                     +---------------------+

Project Structure
day-03-python-etl/
|
+-- README.md
|
+-- python/
|   +-- etl_pipeline.py
|   +-- extract.py
|   +-- transform.py
|   +-- validate.py
|   +-- load.py
|
+-- config/
|   +-- config.py
|
+-- output/
|   +-- etl_run_report.csv
|
+-- logs/
|   +-- etl.log
|
+-- screenshots/


The processed dataset is stored outside the Day 3 folder:

data/
|
+-- processed/
    +-- ecommerce_clean.csv


The raw dataset remains unchanged:

data/raw/ecommerce.csv

Python Modules
etl_pipeline.py

The main orchestration script.

It controls the sequence:

Extract
   |
   v
Transform
   |
   v
Validate
   |
   v
Load


It also handles pipeline-level logging, errors, execution timing, and the ETL run report.

extract.py

Responsible for reading the raw CSV.

transform.py

Responsible for data cleaning, transformation, business rules, and financial calculations.

validate.py

Responsible for validating the transformed dataset before loading.

load.py

Responsible for writing the validated dataset to the processed CSV destination.

config.py

Contains project configuration and project-relative paths.

How to Run the Pipeline

Open PowerShell from the project root:

C:\Users\Durga\Desktop\ecommerce-data-engineering


Activate the virtual environment if necessary:

.\.venv\Scripts\Activate.ps1


Run the ETL pipeline:

python day-03-python-etl\python\etl_pipeline.py

Expected Result

A successful run should report:

Rows extracted : 10,000
Rows transformed: 10,000
Rows loaded    : 10,000
Revenue        : 214,366,057.77


The processed output should be:

data/processed/ecommerce_clean.csv


The ETL report should be:

day-03-python-etl/output/etl_run_report.csv


The log should be:

day-03-python-etl/logs/etl.log

ETL Run Report

The pipeline generates:

etl_run_report.csv


The report records information including:

Pipeline status.

Start time.

End time.

Source file.

Output file.

Source existence.

Extracted rows.

Transformed rows.

Loaded rows.

Column count.

Customer count.

Product count.

Total quantity.

Missing values.

Duplicate order IDs.

Business revenue.

Expected revenue.

Revenue difference.

Validation status.

Error message.

Logging

The pipeline writes execution information to:

day-03-python-etl/logs/etl.log


Logging provides visibility into what the pipeline is doing.

For example:

STEP 1/4 - EXTRACT
STEP 2/4 - TRANSFORM
STEP 3/4 - VALIDATE
STEP 4/4 - LOAD


The log also records validation results and failures.

This is important because production pipelines should not silently fail.

Error Handling

The pipeline uses exception handling to detect failures.

If a stage fails:

The error is logged.

The pipeline stops.

The error is reported clearly.

The run report records the failure.

This makes debugging easier and prevents invalid data from silently moving to the next stage.

Idempotency

The Day 3 pipeline uses a full-refresh approach.

Each successful run:

Raw CSV
   |
   v
Transform
   |
   v
Validate
   |
   v
Overwrite processed CSV


Running the pipeline multiple times produces the same 10,000-row processed dataset.

A second execution was tested successfully:

Rows after second run: 10000


This demonstrates the basic rerunnable behavior of the pipeline.

Incremental processing will be introduced on Day 4.

Validation Results

The Day 3 pipeline successfully validated:

Rows extracted:       10,000
Rows transformed:     10,000
Rows loaded:          10,000

Customers:                 20
Products:                  30
Total quantity:        18,154

Missing values:             0
Duplicate order IDs:        0

Business revenue:
214,366,057.77


Financial validation passed.

The Day 1 business revenue calculation remains:

214,366,057.77


Revenue reconciliation difference:

0.00


PostgreSQL validation also confirmed:

10,000 total rows.

10,000 unique orders.

20 customers.

30 products.

18,154 total quantity.

0 incorrect gross calculations.

0 incorrect discount calculations.

Stored net amount is consistent with gross amount minus discount amount.

Business revenue remains 214,366,057.77.

Financial Rounding Note

The project intentionally preserves the Day 2 financial calculation behavior.

Transaction-level financial fields are calculated using rounded monetary values:

gross_amount
discount_amount
net_amount


The stored relationship is:

net_amount = gross_amount - discount_amount


The authoritative business revenue reconciliation uses the original unrounded business formula:

quantity * unit_price * (1 - discount / 100)


This produces:

214,366,057.77


Different calculation order can produce a one-cent difference on individual transactions. This is a normal financial precision consideration and should not be treated as corrupted data.

Relationship to Day 2

Day 2 created the cleaning and transformation logic.

Day 3 refactored that logic into a reusable ETL architecture.

Day 2
Cleaning Script
      |
      v
Day 3
ETL Pipeline
      |
      v
Day 4
Incremental ETL


Day 2 established data quality.

Day 3 established pipeline structure.

Lessons Learned

Day 3 introduced the following Data Engineering concepts:

ETL architecture.

Extracting data from a source.

Transforming data.

Data validation.

Loading processed data.

Separation of responsibilities.

Reusable Python functions.

Project-relative paths.

Logging.

Exception handling.

ETL execution reports.

Rerunnable pipelines.

Idempotency.

Financial reconciliation.

Cross-system validation.

Next Step - Day 4

Day 4 will introduce:

Incremental ETL

Instead of processing all 10,000 records every time, the pipeline will learn how to identify and process only new data.

The architecture will evolve toward:

Raw Data
   |
   v
Incremental Detection
   |
   v
Transform New Records
   |
   v
Validate
   |
   v
Load New Records
   |
   v
Target


This is an important step toward production-style data pipelines.