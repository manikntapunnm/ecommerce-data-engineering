Day 1 — E-commerce Data Profiling, Data Quality & SQL Analysis
Project Overview

This is Day 1 of the ecommerce-data-engineering project.

The goal of Day 1 is to take raw e-commerce CSV data and perform the initial stages of a data engineering workflow:

Raw Data → Data Profiling → Data Quality → PostgreSQL → SQL Analysis → Visualization

The project uses a realistic e-commerce dataset containing 10,000 orders.

Day 1 Objectives

Load and understand raw CSV data

Profile the dataset using Python and Pandas

Identify missing values and duplicate records

Perform data quality validation

Load the data into PostgreSQL

Perform customer analysis

Perform sales and revenue analysis

Create initial business visualizations

Document the work for GitHub

Dataset
Source

The raw dataset is stored as:

data/raw/ecommerce.csv

Dataset Size

Rows: 10,000

Customers: 20

Products: 30

Categories: 5

Countries: 1

Order dates: 365 days

Columns
Column	Description
order_id	Unique order identifier
order_date	Date of the order
customer_id	Customer identifier
customer_name	Customer name
product_id	Product identifier
product_name	Product name
category	Product category
quantity	Quantity purchased
unit_price	Price per unit
discount	Discount percentage
city	Customer city
state	Customer state
country	Customer country
payment_method	Payment method used
Technologies Used

PostgreSQL — database storage and SQL analysis

Python — data profiling and visualization

Pandas — data handling

Matplotlib — visualization

Seaborn — statistical visualization

CSV — raw data source

Git/GitHub — version control and portfolio

VS Code — development environment

Project Structure
ecommerce-data-engineering/
│
├── README.md
│
├── data/
│   └── raw/
│       └── ecommerce.csv
│
├── day-01-data-profiling/
│   │
│   ├── README.md
│   │
│   ├── sql/
│   │   ├── 01_table_profile.sql
│   │   ├── 02_data_quality.sql
│   │   ├── 03_customer_analysis.sql
│   │   └── 04_sales_analysis.sql
│   │
│   ├── python/
│   │   ├── data_profiling.py
│   │   ├── sales_visualization.py
│   │   └── business_visualizations.py
│   │
│   ├── screenshots/
│   │   ├── sales_distribution.png
│   │   ├── category_revenue.png
│   │   └── monthly_revenue.png
│   │
│   └── output/
│       ├── data_profile.csv
│       └── data_quality_report.csv
│
└── .gitignore

1. Data Profiling

Python and Pandas were used to profile the raw e-commerce dataset.

The profiling process checked:

Number of rows

Number of columns

Data types

Missing values

Duplicate records

Unique values

Numerical statistics

Category distribution

Payment method distribution

Customer count

Product count

The generated profile is stored in:

day-01-data-profiling/output/data_profile.csv

2. Data Quality

Data quality checks were performed using Python and PostgreSQL.

Data Quality Results
Check	Result
Missing order_id	0
Missing order_date	0
Missing customer_id	0
Missing customer_name	0
Missing product_id	0
Missing product_name	0
Missing category	0
Missing quantity	0
Missing unit_price	0
Missing discount	0
Missing city	0
Missing state	0
Missing country	0
Missing payment_method	0
Duplicate order IDs	0
Invalid quantity	0
Invalid unit price	0
Invalid discount	0
Result

18/18 data quality checks passed.

The dataset contains:

No missing values

No duplicate order IDs

No invalid quantities

No invalid unit prices

No invalid discount percentages

The generated report is stored in:

day-01-data-profiling/output/data_quality_report.csv

3. PostgreSQL

The raw CSV data was loaded into PostgreSQL.

Database
ecommerce_db

Table
ecommerce

Records Loaded
10,000


The PostgreSQL table was then used for SQL-based data quality and business analysis.

4. Customer Analysis

Customer-level SQL analysis was performed to understand order volume, quantity purchased, and customer spending.

Total Customers
20

Example Customer Results
Customer	Orders	Quantity
Swathi Rao	542	977
Vikram Singh	521	959
Ravi Teja	—	959
Kavya Nair	—	934

Customer spending analysis was calculated using discount-adjusted revenue.

Revenue Formula
Revenue =
quantity × unit_price × (1 - discount / 100)

5. Sales Analysis

The sales analysis calculated the major business metrics.

Key Metrics
Metric	Result
Total Orders	10,000
Total Customers	20
Total Quantity Sold	18,154
Total Revenue	₹214,366,057.77
Average Order Value	₹21,436.61
6. Revenue by Category

The SQL analysis calculated revenue for each product category.

Category	Revenue
Electronics	₹108,518,542.14
Furniture	₹70,294,383.65
Home Appliances	₹22,845,946.18
Fashion	₹9,266,157.72

The complete category result is generated directly from PostgreSQL.

7. Revenue by State

The analysis also calculated revenue by customer state.

State	Revenue
Tamil Nadu	₹31,892,650.94
Andhra Pradesh	₹31,267,045.92
Telangana	₹30,044,840.12
Karnataka	₹21,914,005.74

The visualization provides a graphical view of the state-level revenue distribution.

8. Revenue by Payment Method

Revenue was also analyzed based on payment method.

Payment Method	Revenue
Net Banking	₹46,550,925.23
UPI	₹45,713,464.06
Cash on Delivery	₹41,884,930.72
Debit Card	₹40,664,058.89
9. SQL Analysis

The following SQL files were created for Day 1:

01_table_profile.sql

Used to inspect the PostgreSQL table structure and basic table information.

02_data_quality.sql

Used to validate:

Missing values

Duplicate order IDs

Invalid quantities

Invalid prices

Invalid discounts

03_customer_analysis.sql

Used for:

Customer count

Orders per customer

Quantity purchased by customer

Customer spending

Average order value

04_sales_analysis.sql

Used for:

Total revenue

Total quantity sold

Total orders

Average order value

Revenue by category

Revenue by product

Monthly revenue

Revenue by state

Revenue by payment method

10. Python Analysis
data_profiling.py

Performs:

Dataset profiling

Missing-value analysis

Duplicate detection

Unique-value analysis

Statistical analysis

Data quality validation

CSV report generation

Generated files:

data_profile.csv
data_quality_report.csv

sales_visualization.py

Creates the state-level revenue visualization.

business_visualizations.py

Creates:

Revenue by state

Revenue by category

Monthly revenue trend

11. Visualizations
Revenue by State

Revenue by Category

Monthly Revenue Trend

12. Day 1 Data Engineering Workflow
                    Raw CSV
                       │
                       ▼
              Python / Pandas
                       │
                       ▼
                Data Profiling
                       │
                       ▼
                Data Quality
                       │
                       ▼
                 PostgreSQL
                       │
                       ▼
                 SQL Analysis
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Customers      Sales       Revenue
          │            │            │
          └────────────┼────────────┘
                       ▼
                Visualization

13. Key Learnings

During Day 1, the following data engineering concepts were practiced:

Working with raw CSV data

Building a reproducible Python profiling process

Understanding data types

Detecting missing values

Detecting duplicate records

Implementing basic data quality rules

Loading CSV data into PostgreSQL

Writing analytical SQL queries

Calculating business metrics

Applying discount-aware revenue calculations

Creating visual evidence with Python

Organizing a data engineering project for GitHub

14. Future Project Roadmap

This project will be expanded over the next 30 days.

Planned technologies include:

Power BI
Python ETL
Airflow
Docker
AWS S3
AWS RDS
CloudWatch
Data Warehouse


These technologies will be introduced progressively as they become relevant to the project architecture.

15. Day 1 Status
✅ Raw CSV generated
✅ 10,000 records created
✅ Python environment configured
✅ Pandas profiling completed
✅ Data profile generated
✅ Data quality report generated
✅ PostgreSQL database created
✅ PostgreSQL table created
✅ 10,000 records loaded
✅ Data quality validation completed
✅ Customer analysis completed
✅ Sales analysis completed
✅ Revenue calculations completed
✅ Business visualizations created
✅ Day 1 documentation completed

Conclusion

Day 1 established the foundation for the ecommerce-data-engineering project by taking raw e-commerce data through profiling, quality validation, PostgreSQL ingestion, SQL analysis, and initial visualization.

The next stages of the project will build on this foundation by introducing ETL pipelines, orchestration, cloud storage, monitoring, and data warehouse concepts.