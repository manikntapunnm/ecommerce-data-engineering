"""
Day 2 - Data Cleaning & Transformation

This script:
1. Loads the raw e-commerce CSV.
2. Inspects the raw dataset.
3. Standardizes column names.
4. Converts data types.
5. Validates business rules.
6. Standardizes text fields.
7. Removes duplicate records.
8. Handles missing values.
9. Creates calculated financial columns.
10. Validates the cleaned dataset.
11. Performs revenue reconciliation.
12. Saves the cleaned dataset and cleaning report.

The script is designed to be run from the project root.
"""

from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "ecommerce.csv"

PROCESSED_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ecommerce_clean.csv"
)

REPORT_PATH = (
    PROJECT_ROOT
    / "day-02-data-cleaning"
    / "output"
    / "cleaning_report.csv"
)


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def standardize_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names by:
    - removing leading/trailing whitespace
    - converting to lowercase
    - replacing spaces with underscores
    """

    dataframe = dataframe.copy()

    dataframe.columns = (
        dataframe.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    return dataframe


def standardize_text_columns(
    dataframe: pd.DataFrame,
    text_columns: list[str],
) -> pd.DataFrame:
    """
    Standardize text columns by:
    - converting values to strings
    - removing leading/trailing whitespace
    - collapsing repeated internal whitespace
    """

    dataframe = dataframe.copy()

    for column in text_columns:
        if column in dataframe.columns:
            dataframe[column] = (
                dataframe[column]
                .astype("string")
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
            )

    return dataframe


def add_report_row(
    report_rows: list[dict],
    check_name: str,
    before_value,
    after_value,
    status: str,
    details: str,
) -> None:
    """
    Add one validation/cleaning result to the report.
    """

    report_rows.append(
        {
            "check_name": check_name,
            "before_value": before_value,
            "after_value": after_value,
            "status": status,
            "details": details,
        }
    )


def round_currency(value) -> Decimal:
    """
    Round a monetary value to two decimal places using
    decimal ROUND_HALF_UP rounding.

    Decimal is used instead of binary floating-point arithmetic
    so that currency calculations are deterministic.
    """

    return Decimal(str(value)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


# ---------------------------------------------------------------------------
# Validation functions
# ---------------------------------------------------------------------------

def validate_required_columns(dataframe: pd.DataFrame) -> None:
    """
    Verify that all expected columns are present.
    """

    required_columns = {
        "order_id",
        "order_date",
        "customer_id",
        "customer_name",
        "product_id",
        "product_name",
        "category",
        "quantity",
        "unit_price",
        "discount",
        "city",
        "state",
        "country",
        "payment_method",
    }

    actual_columns = set(dataframe.columns)

    missing_columns = required_columns - actual_columns

    if missing_columns:
        raise ValueError(
            "Required columns are missing from the dataset: "
            f"{sorted(missing_columns)}"
        )


def validate_business_rules(dataframe: pd.DataFrame) -> dict:
    """
    Validate business rules on the cleaned dataset.

    Returns a dictionary containing the number of invalid values
    found for each rule.
    """

    validation_results = {}

    validation_results["invalid_order_id"] = int(
        (dataframe["order_id"] <= 0).sum()
    )

    validation_results["invalid_customer_id"] = int(
        (dataframe["customer_id"] <= 0).sum()
    )

    validation_results["invalid_product_id"] = int(
        (dataframe["product_id"] <= 0).sum()
    )

    validation_results["invalid_quantity"] = int(
        (dataframe["quantity"] <= 0).sum()
    )

    validation_results["invalid_unit_price"] = int(
        (dataframe["unit_price"] < 0).sum()
    )

    validation_results["invalid_discount"] = int(
        (
            (dataframe["discount"] < 0)
            | (dataframe["discount"] > 100)
        ).sum()
    )

    validation_results["invalid_order_dates"] = int(
        dataframe["order_date"].isna().sum()
    )

    return validation_results


# ---------------------------------------------------------------------------
# Financial calculation functions
# ---------------------------------------------------------------------------

def calculate_gross_amount(
    quantity,
    unit_price,
) -> Decimal:
    """
    Calculate gross transaction amount.

    Formula:

        gross_amount = quantity * unit_price

    The result is rounded to two decimal places.
    """

    quantity_decimal = Decimal(str(quantity))
    unit_price_decimal = Decimal(str(unit_price))

    return round_currency(
        quantity_decimal * unit_price_decimal
    )


def calculate_discount_amount(
    gross_amount,
    discount,
) -> Decimal:
    """
    Calculate discount amount from gross amount.

    Formula:

        discount_amount =
            gross_amount * discount / 100

    The result is rounded to two decimal places.
    """

    gross_decimal = Decimal(str(gross_amount))
    discount_decimal = Decimal(str(discount))

    return round_currency(
        gross_decimal
        * discount_decimal
        / Decimal("100")
    )


def calculate_net_amount(
    gross_amount,
    discount_amount,
) -> Decimal:
    """
    Calculate net transaction amount.

    Formula:

        net_amount = gross_amount - discount_amount

    The result is rounded to two decimal places.
    """

    gross_decimal = Decimal(str(gross_amount))
    discount_decimal = Decimal(str(discount_amount))

    return round_currency(
        gross_decimal - discount_decimal
    )


def calculate_financial_columns(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create gross_amount, discount_amount and net_amount
    using Decimal-based currency calculations.
    """

    dataframe = dataframe.copy()

    # -----------------------------------------------------------------------
    # Gross amount
    # -----------------------------------------------------------------------

    dataframe["gross_amount"] = [
        calculate_gross_amount(
            quantity,
            unit_price,
        )
        for quantity, unit_price in zip(
            dataframe["quantity"],
            dataframe["unit_price"],
        )
    ]

    # -----------------------------------------------------------------------
    # Discount amount
    # -----------------------------------------------------------------------

    dataframe["discount_amount"] = [
        calculate_discount_amount(
            gross_amount,
            discount,
        )
        for gross_amount, discount in zip(
            dataframe["gross_amount"],
            dataframe["discount"],
        )
    ]

    # -----------------------------------------------------------------------
    # Net amount
    # -----------------------------------------------------------------------

    dataframe["net_amount"] = [
        calculate_net_amount(
            gross_amount,
            discount_amount,
        )
        for gross_amount, discount_amount in zip(
            dataframe["gross_amount"],
            dataframe["discount_amount"],
        )
    ]

    return dataframe


# ---------------------------------------------------------------------------
# Main cleaning pipeline
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Run the complete Day 2 data-cleaning pipeline.
    """

    print("=" * 70)
    print("DAY 2 - E-COMMERCE DATA CLEANING PIPELINE")
    print("=" * 70)

    # -----------------------------------------------------------------------
    # 1. Check input file
    # -----------------------------------------------------------------------

    print("\n[1/10] Checking input file...")

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset was not found:\n{RAW_DATA_PATH}"
        )

    print(f"Input file: {RAW_DATA_PATH}")

    # -----------------------------------------------------------------------
    # 2. Load raw dataset
    # -----------------------------------------------------------------------

    print("\n[2/10] Loading raw dataset...")

    dataframe = pd.read_csv(RAW_DATA_PATH)

    original_row_count = len(dataframe)
    original_column_count = len(dataframe.columns)

    print(f"Rows loaded: {original_row_count:,}")
    print(f"Columns loaded: {original_column_count}")

    # -----------------------------------------------------------------------
    # 3. Standardize column names
    # -----------------------------------------------------------------------

    print("\n[3/10] Standardizing column names...")

    dataframe = standardize_column_names(dataframe)

    validate_required_columns(dataframe)

    print("Column names standardized successfully.")

    print("Columns:")

    for column in dataframe.columns:
        print(f"  - {column}")

    # -----------------------------------------------------------------------
    # 4. Convert data types
    # -----------------------------------------------------------------------

    print("\n[4/10] Converting data types...")

    dataframe["order_date"] = pd.to_datetime(
        dataframe["order_date"],
        errors="coerce",
    )

    dataframe["order_id"] = pd.to_numeric(
        dataframe["order_id"],
        errors="coerce",
    )

    dataframe["customer_id"] = pd.to_numeric(
        dataframe["customer_id"],
        errors="coerce",
    )

    dataframe["product_id"] = pd.to_numeric(
        dataframe["product_id"],
        errors="coerce",
    )

    dataframe["quantity"] = pd.to_numeric(
        dataframe["quantity"],
        errors="coerce",
    )

    dataframe["unit_price"] = pd.to_numeric(
        dataframe["unit_price"],
        errors="coerce",
    )

    dataframe["discount"] = pd.to_numeric(
        dataframe["discount"],
        errors="coerce",
    )

    print("Data type conversion completed.")

    # -----------------------------------------------------------------------
    # 5. Standardize text fields
    # -----------------------------------------------------------------------

    print("\n[5/10] Standardizing text fields...")

    text_columns = [
        "customer_name",
        "product_name",
        "category",
        "city",
        "state",
        "country",
        "payment_method",
    ]

    dataframe = standardize_text_columns(
        dataframe,
        text_columns,
    )

    print("Text fields standardized.")

    # -----------------------------------------------------------------------
    # 6. Handle missing values
    # -----------------------------------------------------------------------

    print("\n[6/10] Checking missing values...")

    missing_before = int(
        dataframe.isna().sum().sum()
    )

    missing_by_column = dataframe.isna().sum()

    for column, missing_count in missing_by_column.items():

        if missing_count > 0:
            print(
                f"  WARNING: {column} contains "
                f"{missing_count} missing value(s)."
            )

    # Critical fields cannot safely be fabricated.
    critical_columns = [
        "order_id",
        "order_date",
        "customer_id",
        "product_id",
        "quantity",
        "unit_price",
        "discount",
    ]

    critical_missing = dataframe[critical_columns].isna().sum()

    critical_missing_total = int(
        critical_missing.sum()
    )

    if critical_missing_total > 0:
        raise ValueError(
            "Critical columns contain missing or invalid values "
            "after type conversion:\n"
            f"{critical_missing[critical_missing > 0]}"
        )

    # Descriptive fields can safely use Unknown.
    descriptive_text_columns = [
        "customer_name",
        "product_name",
        "category",
        "city",
        "state",
        "country",
        "payment_method",
    ]

    for column in descriptive_text_columns:

        dataframe[column] = dataframe[column].fillna(
            "Unknown"
        )

    missing_after = int(
        dataframe.isna().sum().sum()
    )

    print(
        f"Missing values before cleaning: "
        f"{missing_before:,}"
    )

    print(
        f"Missing values after cleaning:  "
        f"{missing_after:,}"
    )

    # -----------------------------------------------------------------------
    # 7. Handle duplicate records
    # -----------------------------------------------------------------------

    print("\n[7/10] Checking duplicate records...")

    duplicate_rows = int(
        dataframe.duplicated().sum()
    )

    print(
        f"Duplicate complete rows found: "
        f"{duplicate_rows:,}"
    )

    if duplicate_rows > 0:

        dataframe = dataframe.drop_duplicates().copy()

    duplicate_order_ids = int(
        dataframe["order_id"].duplicated().sum()
    )

    print(
        "Duplicate order IDs after duplicate-row removal: "
        f"{duplicate_order_ids:,}"
    )

    if duplicate_order_ids > 0:

        raise ValueError(
            "Duplicate order IDs remain after removing "
            "duplicate rows. The dataset requires "
            "investigation before continuing."
        )

    # -----------------------------------------------------------------------
    # 8. Validate business rules
    # -----------------------------------------------------------------------

    print("\n[8/10] Validating business rules...")

    validation_results = validate_business_rules(
        dataframe
    )

    for check_name, invalid_count in validation_results.items():

        print(
            f"  {check_name}: {invalid_count}"
        )

    total_invalid_values = sum(
        validation_results.values()
    )

    if total_invalid_values > 0:

        raise ValueError(
            "Business-rule validation failed. "
            f"Total invalid values: "
            f"{total_invalid_values}"
        )

    print(
        "All business-rule validations passed."
    )

    # -----------------------------------------------------------------------
    # 9. Create calculated financial columns
    # -----------------------------------------------------------------------

    print(
        "\n[9/10] Creating calculated financial columns..."
    )

    dataframe = calculate_financial_columns(
        dataframe
    )

    # -----------------------------------------------------------------------
    # Revenue reconciliation
    # -----------------------------------------------------------------------

    # This reproduces the Day 1 revenue calculation.
    #
    # IMPORTANT:
    # Day 1 calculated revenue is based on the original
    # business formula BEFORE transaction-level rounding.

    unrounded_net_revenue = (
        dataframe["quantity"]
        * dataframe["unit_price"]
        * (
            1
            - dataframe["discount"]
            / 100.0
        )
    ).sum()

    # Convert Decimal transaction amounts to a Decimal total.
    rounded_transaction_revenue = sum(
        dataframe["net_amount"]
    )

    print("\nRevenue reconciliation:")

    print(
        f"  Unrounded calculated revenue : "
        f"{unrounded_net_revenue:,.2f}"
    )

    print(
        f"  Rounded transaction revenue  : "
        f"{rounded_transaction_revenue:,.2f}"
    )

    rounding_difference = (
        float(rounded_transaction_revenue)
        - float(unrounded_net_revenue)
    )

    print(
        f"  Rounding difference           : "
        f"{rounding_difference:,.2f}"
    )

    # -----------------------------------------------------------------------
    # 10. Final validation
    # -----------------------------------------------------------------------

    print(
        "\n[10/10] Performing final validation..."
    )

    final_row_count = len(dataframe)

    final_column_count = len(
        dataframe.columns
    )

    final_missing_values = int(
        dataframe.isna().sum().sum()
    )

    final_duplicate_rows = int(
        dataframe.duplicated().sum()
    )

    final_duplicate_order_ids = int(
        dataframe["order_id"].duplicated().sum()
    )

    invalid_net_amounts = int(
        (
            dataframe["net_amount"]
            < Decimal("0.00")
        ).sum()
    )

    # -----------------------------------------------------------------------
    # Validation failures
    # -----------------------------------------------------------------------

    if final_missing_values > 0:

        raise ValueError(
            f"Final dataset still contains "
            f"{final_missing_values} missing values."
        )

    if final_duplicate_rows > 0:

        raise ValueError(
            f"Final dataset still contains "
            f"{final_duplicate_rows} duplicate rows."
        )

    if final_duplicate_order_ids > 0:

        raise ValueError(
            f"Final dataset contains "
            f"{final_duplicate_order_ids} "
            f"duplicate order IDs."
        )

    if invalid_net_amounts > 0:

        raise ValueError(
            f"Final dataset contains "
            f"{invalid_net_amounts} "
            f"negative net amounts."
        )

    # -----------------------------------------------------------------------
    # Create output directories
    # -----------------------------------------------------------------------

    PROCESSED_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -----------------------------------------------------------------------
    # Save cleaned dataset
    # -----------------------------------------------------------------------

    dataframe.to_csv(
        PROCESSED_DATA_PATH,
        index=False,
    )

    # -----------------------------------------------------------------------
    # Build cleaning report
    # -----------------------------------------------------------------------

    report_rows = []

    add_report_row(
        report_rows,
        "Input row count",
        original_row_count,
        final_row_count,
        "PASS",
        "Rows in raw dataset compared with final cleaned dataset.",
    )

    add_report_row(
        report_rows,
        "Input column count",
        original_column_count,
        final_column_count,
        "PASS",
        "Final dataset contains original columns plus calculated columns.",
    )

    add_report_row(
        report_rows,
        "Missing values",
        missing_before,
        missing_after,
        "PASS" if missing_after == 0 else "FAIL",
        "Missing-value validation after cleaning.",
    )

    add_report_row(
        report_rows,
        "Duplicate complete rows",
        duplicate_rows,
        final_duplicate_rows,
        "PASS" if final_duplicate_rows == 0 else "FAIL",
        "Duplicate complete rows were removed.",
    )

    add_report_row(
        report_rows,
        "Duplicate order IDs",
        duplicate_order_ids,
        final_duplicate_order_ids,
        "PASS" if final_duplicate_order_ids == 0 else "FAIL",
        "Order IDs must uniquely identify orders.",
    )

    add_report_row(
        report_rows,
        "Invalid order IDs",
        validation_results["invalid_order_id"],
        0,
        "PASS",
        "Order IDs must be greater than zero.",
    )

    add_report_row(
        report_rows,
        "Invalid customer IDs",
        validation_results["invalid_customer_id"],
        0,
        "PASS",
        "Customer IDs must be greater than zero.",
    )

    add_report_row(
        report_rows,
        "Invalid product IDs",
        validation_results["invalid_product_id"],
        0,
        "PASS",
        "Product IDs must be greater than zero.",
    )

    add_report_row(
        report_rows,
        "Invalid quantity",
        validation_results["invalid_quantity"],
        0,
        "PASS",
        "Quantity must be greater than zero.",
    )

    add_report_row(
        report_rows,
        "Invalid unit price",
        validation_results["invalid_unit_price"],
        0,
        "PASS",
        "Unit price cannot be negative.",
    )

    add_report_row(
        report_rows,
        "Invalid discount",
        validation_results["invalid_discount"],
        0,
        "PASS",
        "Discount must be between 0 and 100 percent.",
    )

    add_report_row(
        report_rows,
        "Invalid order dates",
        validation_results["invalid_order_dates"],
        0,
        "PASS",
        "Order dates must be valid dates.",
    )

    add_report_row(
        report_rows,
        "Negative net amounts",
        invalid_net_amounts,
        0,
        "PASS" if invalid_net_amounts == 0 else "FAIL",
        "Net amount must not be negative.",
    )

    # Calculate totals as Decimal values.
    gross_total = sum(
        dataframe["gross_amount"]
    )

    discount_total = sum(
        dataframe["discount_amount"]
    )

    net_total = sum(
        dataframe["net_amount"]
    )

    add_report_row(
        report_rows,
        "Calculated gross amount",
        None,
        f"{gross_total:.2f}",
        "PASS",
        "gross_amount = quantity * unit_price, rounded to two decimals.",
    )

    add_report_row(
        report_rows,
        "Calculated discount amount",
        None,
        f"{discount_total:.2f}",
        "PASS",
        "discount_amount = gross_amount * discount / 100, rounded to two decimals.",
    )

    add_report_row(
        report_rows,
        "Calculated net amount",
        None,
        f"{net_total:.2f}",
        "PASS",
        "net_amount = gross_amount - discount_amount, rounded to two decimals.",
    )

    add_report_row(
        report_rows,
        "Unrounded revenue reconciliation",
        None,
        f"{unrounded_net_revenue:.2f}",
        "PASS",
        "Revenue calculated using the Day 1 business formula before transaction-level rounding.",
    )

    add_report_row(
        report_rows,
        "Transaction rounding difference",
        None,
        f"{rounding_difference:.2f}",
        "PASS",
        "Difference caused by rounding individual transaction amounts to two decimal places.",
    )

    cleaning_report = pd.DataFrame(
        report_rows
    )

    cleaning_report.to_csv(
        REPORT_PATH,
        index=False,
    )

    # -----------------------------------------------------------------------
    # Final summary
    # -----------------------------------------------------------------------

    print("\n" + "=" * 70)
    print(
        "CLEANING PIPELINE COMPLETED SUCCESSFULLY"
    )
    print("=" * 70)

    print(
        f"\nOriginal rows : "
        f"{original_row_count:,}"
    )

    print(
        f"Final rows    : "
        f"{final_row_count:,}"
    )

    print(
        f"Original cols : "
        f"{original_column_count}"
    )

    print(
        f"Final cols    : "
        f"{final_column_count}"
    )

    print("\nCalculated columns:")

    print("  - gross_amount")
    print("  - discount_amount")
    print("  - net_amount")

    print("\nOutput files:")

    print(
        f"  Clean dataset : "
        f"{PROCESSED_DATA_PATH}"
    )

    print(
        f"  Cleaning report: "
        f"{REPORT_PATH}"
    )

    print("\nFinancial totals:")

    print(
        f"  Gross amount    : "
        f"{gross_total:,.2f}"
    )

    print(
        f"  Discount amount : "
        f"{discount_total:,.2f}"
    )

    print(
        f"  Net amount      : "
        f"{net_total:,.2f}"
    )

    print(
        "\nDay 2 cleaning pipeline finished."
    )


# ---------------------------------------------------------------------------
# Script entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
