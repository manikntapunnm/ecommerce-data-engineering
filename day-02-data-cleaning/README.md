Day 2 — Data Cleaning & Transformation
Project

ecommerce-data-engineering

Day 2 focuses on transforming the raw e-commerce dataset into a validated, analysis-ready dataset using Python and Pandas.

Objective

The goal of Day 2 is to build a reusable data-cleaning pipeline:

Raw CSV
   ↓
Load Dataset
   ↓
Standardize Columns
   ↓
Convert Data Types
   ↓
Clean Text Fields
   ↓
Handle Missing Values
   ↓
Remove Duplicate Records
   ↓
Validate Business Rules
   ↓
Calculate Financial Columns
   ↓
Validate Clean Dataset
   ↓
Save Processed CSV
   ↓
Load into PostgreSQL
   ↓
SQL Validation

Technologies

Python

Pandas

PostgreSQL

SQL

CSV

Git

VS Code

PowerShell

Input Dataset

The raw dataset is located at:

data/raw/ecommerce.csv


The dataset contains:

10,000 rows

14 source columns

20 customers

30 products

5 product categories

365 order dates

Source Columns
order_id
order_date
customer_id
customer_name
product_id
product_name
category
quantity
unit_price
discount
city
state
country
payment_method

Cleaning Operations
Column Name Standardization

Column names are:

converted to lowercase

stripped of leading/trailing whitespace

converted to underscore-separated names

Example:

Order Date


becomes:

order_date

Data Type Conversion

The pipeline converts:

order_date  → datetime
order_id    → numeric
customer_id → numeric
product_id  → numeric
quantity    → numeric
unit_price  → numeric
discount    → numeric

Text Standardization

Text columns are cleaned by:

removing leading/trailing whitespace

collapsing repeated whitespace

standardizing missing descriptive values to Unknown

Missing Values

Critical fields are not artificially populated.

The pipeline stops if critical fields such as IDs, dates, quantity, unit price, or discount contain invalid/missing values after conversion.

Descriptive text fields can use:

Unknown


when appropriate.

Duplicate Records

The pipeline checks:

duplicate complete records

duplicate order_id values

Duplicate complete rows are removed.

Duplicate order IDs remaining after duplicate-row removal cause the pipeline to stop for investigation.

Business Rules

The pipeline validates:

order_id > 0
customer_id > 0
product_id > 0
quantity > 0
unit_price >= 0
0 <= discount <= 100
order_date must be valid

Financial Transformations

Three calculated columns are created.

Gross Amount
gross_amount = quantity × unit_price

Discount Amount
discount_amount = gross_amount × discount / 100

Net Amount
net_amount = gross_amount - discount_amount


Transaction-level monetary values are stored with two decimal places.

Python uses Decimal with ROUND_HALF_UP to make currency rounding explicit and deterministic.

Revenue Reconciliation

Day 1 calculated revenue was:

214,366,057.77


Day 2 independently recalculates the original business formula:

quantity × unit_price × (1 - discount / 100)


The cleaned dataset preserves this calculation.

Expected reconciliation:

Day 1 revenue       : 214,366,057.77
Day 2 equivalent    : 214,366,057.77
Difference          : 0.00


The transaction-level net_amount total may differ slightly because each transaction is rounded to two decimal places before aggregation.

This distinction is intentional and documented.

Output Dataset

The cleaned dataset is saved to:

data/processed/ecommerce_clean.csv


The final dataset contains:

14 original columns
+
3 calculated columns
=
17 columns


Calculated columns:

gross_amount
discount_amount
net_amount

Cleaning Report

The pipeline generates:

day-02-data-cleaning/output/cleaning_report.csv


The report records:

row counts

column counts

missing-value checks

duplicate checks

ID validation

quantity validation

unit-price validation

discount validation

date validation

negative net-amount validation

financial totals

revenue reconciliation

transaction rounding difference

PostgreSQL Validation

The cleaned CSV is loaded into:

ecommerce_db


Table:

ecommerce_clean


The SQL validation script is:

day-02-data-cleaning/sql/01_clean_data_validation.sql


The validation checks:

total row count

table structure

duplicate order IDs

missing values

invalid IDs

invalid quantities

invalid prices

invalid discounts

negative financial amounts

incorrect gross calculations

incorrect discount calculations

incorrect net calculations

revenue reconciliation

Expected row count:

10,000


Expected duplicate order IDs:

0


Expected financial calculation errors:

0

Project Structure
day-02-data-cleaning/
│
├── README.md
│
├── python/
│   └── data_cleaning.py
│
├── sql/
│   └── 01_clean_data_validation.sql
│
├── output/
│   └── cleaning_report.csv
│
└── screenshots/


Processed data:

data/
│
├── raw/
│   └── ecommerce.csv
│
└── processed/
    └── ecommerce_clean.csv

How to Run

From the project root:

python .\day-02-data-cleaning\python\data_cleaning.py


The pipeline creates or updates:

data/processed/ecommerce_clean.csv
day-02-data-cleaning/output/cleaning_report.csv

PostgreSQL Validation

Start PostgreSQL with:

& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d ecommerce_db


Then execute:

\i 'C:/Users/Durga/Desktop/ecommerce-data-engineering/day-02-data-cleaning/sql/01_clean_data_validation.sql'

Day 2 Result

The Day 2 pipeline transforms the original raw CSV into a cleaned and validated dataset while preserving the original Day 1 business revenue calculation.

The processed dataset is ready for the next stage of the project:

Day 3 — Python ETL Pipeline