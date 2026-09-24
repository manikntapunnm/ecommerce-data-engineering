Day 4 — Incremental ETL Pipeline
Overview

Day 4 extends the ecommerce data engineering project by implementing an incremental ETL pipeline.

Instead of processing the complete ecommerce dataset every time, the pipeline uses a watermark based on order_id to identify and process only new records.

The pipeline follows:

Raw CSV
   ↓
Watermark
   ↓
Extract new records
   ↓
Transform
   ↓
Validate
   ↓
Load into processed dataset
   ↓
Verify load
   ↓
Update watermark
   ↓
Create run report

Project Structure
day-04-incremental-etl/
│
├── python/
│   ├── extract_incremental.py
│   ├── transform_incremental.py
│   ├── validate_incremental.py
│   ├── load_incremental.py
│   ├── incremental_etl.py
│   └── failure_test.py
│
├── state/
│   └── watermark.txt
│
├── logs/
│   └── incremental_etl.log
│
└── output/
    └── incremental_run_report.csv


Generated runtime files under logs/ and output/ are excluded from Git.

Incremental Processing

The pipeline stores the last successfully processed order_id in:

day-04-incremental-etl/state/watermark.txt


For example:

12000


The extraction stage selects records where:

order_id > watermark


After successful processing and load, the watermark is updated to the highest successfully processed order_id.

Example:

Watermark before: 12000
New records:      5
Watermark after:  12005

Transformation

Each incremental record receives the following calculated fields:

Gross Amount
gross_amount = quantity × unit_price

Discount Amount
discount_amount = gross_amount × discount / 100

Net Amount
net_amount = gross_amount - discount_amount

Validation

The validation stage checks:

Required columns exist

Missing values

Duplicate order_id values

Valid order IDs

Valid customer IDs

Valid product IDs

Positive quantities

Non-negative unit prices

Discounts between 0 and 100

Valid order dates

Correct gross amount calculations

Correct discount calculations

Correct net amount calculations

The pipeline also independently calculates incremental business revenue from:

quantity × unit_price × (1 - discount / 100)


The watermark is updated only after validation and load verification succeed.

Load Logic

The loader reads the existing processed dataset and checks the incoming records against existing order_id values.

If an order_id already exists in the target, that record is skipped.

This prevents duplicate orders from being added to the processed dataset.

Load Verification

After loading, the pipeline verifies that all incremental order_id values exist in the processed dataset.

If any expected order is missing, the pipeline fails and the watermark is not advanced.

Failure Handling

The pipeline uses try/except error handling around the complete ETL process.

If any stage fails:

Watermark remains unchanged
Pipeline status = FAILED
Error is logged
Run report is created


This prevents the pipeline from incorrectly marking failed records as successfully processed.

Run Reporting

Each pipeline execution creates a CSV run report containing:

Pipeline status

Start and end timestamps

Watermark before processing

Watermark after processing

Source file

Source row count

Extracted row count

Transformed row count

Loaded row count

Validation status

Incremental revenue

Error message

The generated report is stored under:

day-04-incremental-etl/output/

Logging

The pipeline writes timestamped logs for each major ETL stage:

Reading watermark
Extract stage
Transform stage
Validation stage
Load stage
Load verification
Watermark update
Run report


Logs are stored under:

day-04-incremental-etl/logs/

Day 4 Test Results

The initial processed dataset contained:

Processed rows: 12000
Max order_id:   12000
Unique orders:  12000


Five new records were then added to the source dataset.

The incremental pipeline detected and processed:

Rows in source:       12005
Rows extracted:           5
Rows transformed:         5
Rows loaded:              5
Incremental revenue: 76070.00


The watermark was successfully updated:

12000 → 12005


The final processed dataset contained:

Processed rows: 12005
Max order_id:   12005
Unique orders:  12005


A second pipeline execution was then performed.

Because there were no records after order_id = 12005, the pipeline correctly reported:

Rows extracted: 0
Rows transformed: 0
Rows loaded: 0
Watermark: 12005


This confirms that the incremental logic is working and that already-processed records are not reloaded.

How to Run

Activate the virtual environment:

.venv\Scripts\Activate.ps1


Run the complete incremental ETL pipeline:

python day-04-incremental-etl/python/incremental_etl.py


To inspect the watermark:

Get-Content day-04-incremental-etl/state/watermark.txt


To verify the processed dataset:

python -c "import pandas as pd; df=pd.read_csv('data/processed/ecommerce_clean.csv'); print('Processed rows:', len(df)); print('Max order_id:', df['order_id'].max()); print('Unique orders:', df['order_id'].nunique())"

Key Learning

Day 4 demonstrates how an ETL pipeline can move from full-load processing to incremental processing.

The main concepts implemented are:

Watermarks
Incremental extraction
Idempotent loading
Data validation
Load verification
Failure handling
Run reporting
Structured logging


The result is a pipeline that processes only newly arrived ecommerce records while protecting the processed dataset from duplicate loads and preventing the watermark from advancing after a failed run.