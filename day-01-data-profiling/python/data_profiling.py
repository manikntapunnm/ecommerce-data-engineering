import importlib
import os

try:
    pd = importlib.import_module("pandas")
except ImportError as exc:
    raise SystemExit(
        "pandas is required. Install it with: python -m pip install pandas"
    ) from exc


# ---------------------------------------------------------
# E-COMMERCE DATA PROFILING
# Day 1 - Data Engineering Project
# ---------------------------------------------------------

# Project root directory
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

# ---------------------------------------------------------
# Input and Output Paths
# ---------------------------------------------------------

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "ecommerce.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "day-01-data-profiling",
    "output"
)

PROFILE_FILE = os.path.join(
    OUTPUT_DIR,
    "data_profile.csv"
)

QUALITY_FILE = os.path.join(
    OUTPUT_DIR,
    "data_quality_report.csv"
)

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

# Convert order_date from string to datetime
df["order_date"] = pd.to_datetime(df["order_date"])


print("=" * 70)
print("E-COMMERCE DATA PROFILING")
print("=" * 70)


# ---------------------------------------------------------
# 1. Dataset Information
# ---------------------------------------------------------

print("\n1. DATASET INFORMATION")

print(f"Rows       : {df.shape[0]}")
print(f"Columns    : {df.shape[1]}")


# ---------------------------------------------------------
# 2. Column Information
# ---------------------------------------------------------

print("\n2. COLUMN INFORMATION")

print(df.dtypes)


# ---------------------------------------------------------
# 3. Missing Values
# ---------------------------------------------------------

print("\n3. MISSING VALUES")

missing_values = df.isnull().sum()

print(missing_values)


# ---------------------------------------------------------
# 4. Duplicate Records
# ---------------------------------------------------------

print("\n4. DUPLICATE RECORDS")

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows: {duplicate_count}")


# ---------------------------------------------------------
# 5. Unique Values
# ---------------------------------------------------------

print("\n5. UNIQUE VALUES")

print(df.nunique())


# ---------------------------------------------------------
# 6. Numerical Statistics
# ---------------------------------------------------------

print("\n6. NUMERICAL STATISTICS")

print(df.describe())


# ---------------------------------------------------------
# 7. Category Distribution
# ---------------------------------------------------------

print("\n7. CATEGORY DISTRIBUTION")

print(df["category"].value_counts())


# ---------------------------------------------------------
# 8. Payment Method Distribution
# ---------------------------------------------------------

print("\n8. PAYMENT METHOD DISTRIBUTION")

print(df["payment_method"].value_counts())


# ---------------------------------------------------------
# 9. Customer Count
# ---------------------------------------------------------

print("\n9. CUSTOMER ANALYSIS")

print(
    f"Unique customers: {df['customer_id'].nunique()}"
)


# ---------------------------------------------------------
# 10. Product Count
# ---------------------------------------------------------

print("\n10. PRODUCT ANALYSIS")

print(
    f"Unique products: {df['product_id'].nunique()}"
)


# ---------------------------------------------------------
# 11. Data Profile Report
# ---------------------------------------------------------

profile = pd.DataFrame({
    "column_name": df.columns,
    "data_type": [
        str(df[column].dtype)
        for column in df.columns
    ],
    "row_count": len(df),
    "missing_values": [
        df[column].isnull().sum()
        for column in df.columns
    ],
    "unique_values": [
        df[column].nunique()
        for column in df.columns
    ]
})

profile.to_csv(
    PROFILE_FILE,
    index=False
)

print("\nProfile saved to:")
print(PROFILE_FILE)


# =========================================================
# DATA QUALITY REPORT
# =========================================================

print("\n" + "=" * 70)
print("DATA QUALITY CHECKS")
print("=" * 70)

quality_checks = []


# ---------------------------------------------------------
# 1. Missing Values
# ---------------------------------------------------------

for column in df.columns:

    missing_count = df[column].isna().sum()

    quality_checks.append({
        "check_name": f"Missing values - {column}",
        "status": "PASS" if missing_count == 0 else "FAIL",
        "value": int(missing_count)
    })


# ---------------------------------------------------------
# 2. Duplicate Order IDs
# ---------------------------------------------------------

duplicate_orders = df["order_id"].duplicated().sum()

quality_checks.append({
    "check_name": "Duplicate order IDs",
    "status": "PASS" if duplicate_orders == 0 else "FAIL",
    "value": int(duplicate_orders)
})


# ---------------------------------------------------------
# 3. Invalid Quantity
# ---------------------------------------------------------

invalid_quantity = (
    df["quantity"] <= 0
).sum()

quality_checks.append({
    "check_name": "Invalid quantity",
    "status": "PASS" if invalid_quantity == 0 else "FAIL",
    "value": int(invalid_quantity)
})


# ---------------------------------------------------------
# 4. Invalid Unit Price
# ---------------------------------------------------------

invalid_price = (
    df["unit_price"] <= 0
).sum()

quality_checks.append({
    "check_name": "Invalid unit price",
    "status": "PASS" if invalid_price == 0 else "FAIL",
    "value": int(invalid_price)
})


# ---------------------------------------------------------
# 5. Invalid Discount
# ---------------------------------------------------------

invalid_discount = (
    (df["discount"] < 0) |
    (df["discount"] > 100)
).sum()

quality_checks.append({
    "check_name": "Invalid discount",
    "status": "PASS" if invalid_discount == 0 else "FAIL",
    "value": int(invalid_discount)
})


# ---------------------------------------------------------
# Create Quality Report
# ---------------------------------------------------------

quality_report = pd.DataFrame(
    quality_checks
)

quality_report.to_csv(
    QUALITY_FILE,
    index=False
)


print("\nData quality report saved to:")
print(QUALITY_FILE)


print("\nData Quality Summary:")

print(quality_report.to_string(index=False))


# ---------------------------------------------------------
# Completion Message
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("DATA PROFILING COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nGenerated files:")

print(f"1. {PROFILE_FILE}")
print(f"2. {QUALITY_FILE}")
