"""
Day 3 - Python ETL Pipeline
Transform Stage

Responsible for:
    1. Standardizing column names
    2. Converting data types
    3. Standardizing text values
    4. Validating missing values
    5. Validating duplicates
    6. Validating business rules
    7. Creating financial columns
    8. Validating calculated financial columns

The raw CSV is never modified.
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# Required source columns
# -------------------------------------------------------------------

REQUIRED_COLUMNS = [
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
]


# -------------------------------------------------------------------
# Expected business revenue from Day 1
# -------------------------------------------------------------------

EXPECTED_BUSINESS_REVENUE = 214366057.77


# -------------------------------------------------------------------
# Helper function: validate required columns
# -------------------------------------------------------------------

def validate_required_columns(
    dataframe: pd.DataFrame,
) -> None:
    """
    Check that all required source columns exist.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )


# -------------------------------------------------------------------
# Helper function: standardize column names
# -------------------------------------------------------------------

def standardize_column_names(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert column names to lowercase snake_case.
    """

    dataframe = dataframe.copy()

    dataframe.columns = (
        dataframe.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return dataframe


# -------------------------------------------------------------------
# Helper function: convert data types
# -------------------------------------------------------------------

def convert_data_types(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert columns to appropriate data types.
    """

    dataframe = dataframe.copy()

    # Integer columns
    integer_columns = [
        "order_id",
        "customer_id",
        "product_id",
        "quantity",
    ]

    for column in integer_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="raise",
        ).astype("int64")

    # Numeric columns
    numeric_columns = [
        "unit_price",
        "discount",
    ]

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="raise",
        )

    # Date column
    dataframe["order_date"] = pd.to_datetime(
        dataframe["order_date"],
        errors="raise",
    )

    return dataframe


# -------------------------------------------------------------------
# Helper function: standardize text fields
# -------------------------------------------------------------------

def standardize_text_fields(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove unnecessary whitespace from text columns.
    """

    dataframe = dataframe.copy()

    text_columns = [
        "customer_name",
        "product_name",
        "category",
        "city",
        "state",
        "country",
        "payment_method",
    ]

    for column in text_columns:
        dataframe[column] = (
            dataframe[column]
            .astype(str)
            .str.strip()
        )

    return dataframe


# -------------------------------------------------------------------
# Missing-value validation
# -------------------------------------------------------------------

def validate_missing_values(
    dataframe: pd.DataFrame,
) -> int:
    """
    Check for missing values.

    Returns
    -------
    int
        Total number of missing values.
    """

    missing_values = int(
        dataframe.isna().sum().sum()
    )

    if missing_values > 0:
        raise ValueError(
            f"Missing values detected: {missing_values}"
        )

    logger.info(
        "Missing-value validation passed."
    )

    return missing_values


# -------------------------------------------------------------------
# Duplicate validation
# -------------------------------------------------------------------

def validate_duplicates(
    dataframe: pd.DataFrame,
) -> int:
    """
    Check for duplicate complete rows and duplicate order IDs.

    Returns
    -------
    int
        Number of duplicate order IDs.
    """

    duplicate_rows = int(
        dataframe.duplicated().sum()
    )

    if duplicate_rows > 0:
        raise ValueError(
            f"Duplicate complete rows detected: "
            f"{duplicate_rows}"
        )

    duplicate_order_ids = int(
        dataframe["order_id"]
        .duplicated()
        .sum()
    )

    if duplicate_order_ids > 0:
        raise ValueError(
            f"Duplicate order IDs detected: "
            f"{duplicate_order_ids}"
        )

    logger.info(
        "Duplicate validation passed."
    )

    return duplicate_order_ids


# -------------------------------------------------------------------
# Business-rule validation
# -------------------------------------------------------------------

def validate_business_rules(
    dataframe: pd.DataFrame,
) -> None:
    """
    Validate core e-commerce business rules.
    """

    if (dataframe["order_id"] <= 0).any():
        raise ValueError(
            "Invalid order_id detected."
        )

    if (dataframe["customer_id"] <= 0).any():
        raise ValueError(
            "Invalid customer_id detected."
        )

    if (dataframe["product_id"] <= 0).any():
        raise ValueError(
            "Invalid product_id detected."
        )

    if (dataframe["quantity"] <= 0).any():
        raise ValueError(
            "Invalid quantity detected."
        )

    if (dataframe["unit_price"] < 0).any():
        raise ValueError(
            "Invalid unit_price detected."
        )

    if (
        (dataframe["discount"] < 0)
        | (dataframe["discount"] > 100)
    ).any():
        raise ValueError(
            "Invalid discount detected."
        )

    if dataframe["order_date"].isna().any():
        raise ValueError(
            "Invalid order_date detected."
        )

    logger.info(
        "Business-rule validation passed."
    )


# -------------------------------------------------------------------
# Financial transformation
# -------------------------------------------------------------------

def calculate_financial_columns(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create financial columns.

    Calculations:

        gross_amount =
            quantity * unit_price

        discount_amount =
            gross_amount * discount / 100

        net_amount =
            gross_amount - discount_amount

    Monetary values are rounded to two decimal places
    at the transaction level.
    """

    dataframe = dataframe.copy()

    # ---------------------------------------------------------------
    # Calculate raw gross amount first.
    #
    # We intentionally keep this unrounded because the discount
    # calculation must use the same business calculation path.
    # ---------------------------------------------------------------

    gross_raw = (
        dataframe["quantity"]
        * dataframe["unit_price"]
    )

    # ---------------------------------------------------------------
    # Calculate discount from the unrounded gross amount.
    # ---------------------------------------------------------------

    discount_raw = (
        gross_raw
        * dataframe["discount"]
        / 100.0
    )

    # ---------------------------------------------------------------
    # Calculate net amount from the unrounded gross amount.
    # ---------------------------------------------------------------

    net_raw = (
        gross_raw
        - discount_raw
    )

    # ---------------------------------------------------------------
    # Store transaction-level monetary values rounded to 2 decimals.
    # ---------------------------------------------------------------

    dataframe["gross_amount"] = (
        gross_raw.round(2)
    )

    dataframe["discount_amount"] = (
        discount_raw.round(2)
    )

    dataframe["net_amount"] = (
        net_raw.round(2)
    )

    return dataframe


# -------------------------------------------------------------------
# Financial calculation validation
# -------------------------------------------------------------------

def validate_financial_columns(
    dataframe: pd.DataFrame,
) -> dict:
    """
    Validate gross_amount, discount_amount and net_amount.

    The expected values reproduce the exact same calculation
    sequence used by calculate_financial_columns().

    Returns
    -------
    dict
        Financial validation results.
    """

    # ---------------------------------------------------------------
    # Recreate the original unrounded calculations.
    # ---------------------------------------------------------------

    gross_raw = (
        dataframe["quantity"]
        * dataframe["unit_price"]
    )

    discount_raw = (
        gross_raw
        * dataframe["discount"]
        / 100.0
    )

    net_raw = (
        gross_raw
        - discount_raw
    )

    # ---------------------------------------------------------------
    # Apply the same transaction-level rounding.
    # ---------------------------------------------------------------

    expected_gross = (
        gross_raw.round(2)
    )

    expected_discount = (
        discount_raw.round(2)
    )

    expected_net = (
        net_raw.round(2)
    )

    # ---------------------------------------------------------------
    # Compare calculated values.
    #
    # np.isclose() protects the comparison against tiny floating
    # point representation differences.
    # ---------------------------------------------------------------

    incorrect_gross = int(
        (
            ~np.isclose(
                dataframe["gross_amount"],
                expected_gross,
                rtol=0,
                atol=0.005,
            )
        ).sum()
    )

    incorrect_discount = int(
        (
            ~np.isclose(
                dataframe["discount_amount"],
                expected_discount,
                rtol=0,
                atol=0.005,
            )
        ).sum()
    )

    incorrect_net = int(
        (
            ~np.isclose(
                dataframe["net_amount"],
                expected_net,
                rtol=0,
                atol=0.005,
            )
        ).sum()
    )

    # ---------------------------------------------------------------
    # Fail if calculations are incorrect.
    # ---------------------------------------------------------------

    if incorrect_gross > 0:
        raise ValueError(
            f"Incorrect gross calculations: "
            f"{incorrect_gross}"
        )

    if incorrect_discount > 0:
        raise ValueError(
            f"Incorrect discount calculations: "
            f"{incorrect_discount}"
        )

    if incorrect_net > 0:
        raise ValueError(
            f"Incorrect net calculations: "
            f"{incorrect_net}"
        )

    # ---------------------------------------------------------------
    # Revenue reconciliation.
    #
    # IMPORTANT:
    # This reproduces the Day 1 business revenue formula without
    # transaction-level rounding.
    # ---------------------------------------------------------------

    calculated_business_revenue = (
        (
            dataframe["quantity"]
            * dataframe["unit_price"]
            * (
                1
                - dataframe["discount"] / 100.0
            )
        )
        .sum()
    )

    calculated_business_revenue = round(
        float(calculated_business_revenue),
        2,
    )

    revenue_difference = round(
        calculated_business_revenue
        - EXPECTED_BUSINESS_REVENUE,
        2,
    )

    if revenue_difference != 0.00:
        raise ValueError(
            "Revenue reconciliation failed. "
            f"Expected {EXPECTED_BUSINESS_REVENUE:,.2f}, "
            f"calculated "
            f"{calculated_business_revenue:,.2f}, "
            f"difference {revenue_difference:,.2f}"
        )

    logger.info(
        "Financial calculation validation passed."
    )

    logger.info(
        "Day 1 business revenue: %.2f",
        calculated_business_revenue,
    )

    logger.info(
        "Revenue difference: %.2f",
        revenue_difference,
    )

    return {
        "calculated_business_revenue":
            calculated_business_revenue,
        "expected_business_revenue":
            EXPECTED_BUSINESS_REVENUE,
        "revenue_difference":
            revenue_difference,
    }


# -------------------------------------------------------------------
# Main transform function
# -------------------------------------------------------------------

def transform_data(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Execute the complete transformation stage.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Raw extracted DataFrame.

    Returns
    -------
    pd.DataFrame
        Transformed and validated DataFrame.
    """

    logger.info(
        "Starting transform stage."
    )

    logger.info(
        "Transform input: %s rows, %s columns.",
        len(dataframe),
        len(dataframe.columns),
    )

    # ---------------------------------------------------------------
    # Make a copy so the original extracted DataFrame is not changed.
    # ---------------------------------------------------------------

    transformed = dataframe.copy()

    # ---------------------------------------------------------------
    # 1. Standardize column names
    # ---------------------------------------------------------------

    transformed = standardize_column_names(
        transformed
    )

    # ---------------------------------------------------------------
    # 2. Verify required columns
    # ---------------------------------------------------------------

    validate_required_columns(
        transformed
    )

    # ---------------------------------------------------------------
    # 3. Convert data types
    # ---------------------------------------------------------------

    transformed = convert_data_types(
        transformed
    )

    # ---------------------------------------------------------------
    # 4. Standardize text fields
    # ---------------------------------------------------------------

    transformed = standardize_text_fields(
        transformed
    )

    # ---------------------------------------------------------------
    # 5. Validate missing values
    # ---------------------------------------------------------------

    validate_missing_values(
        transformed
    )

    # ---------------------------------------------------------------
    # 6. Validate duplicates
    # ---------------------------------------------------------------

    validate_duplicates(
        transformed
    )

    # ---------------------------------------------------------------
    # 7. Validate business rules
    # ---------------------------------------------------------------

    validate_business_rules(
        transformed
    )

    # ---------------------------------------------------------------
    # 8. Calculate financial columns
    # ---------------------------------------------------------------

    transformed = calculate_financial_columns(
        transformed
    )

    # ---------------------------------------------------------------
    # 9. Validate financial calculations
    # ---------------------------------------------------------------

    financial_results = validate_financial_columns(
        transformed
    )

    # ---------------------------------------------------------------
    # 10. Final validation
    # ---------------------------------------------------------------

    required_output_columns = [
        "gross_amount",
        "discount_amount",
        "net_amount",
    ]

    missing_output_columns = [
        column
        for column in required_output_columns
        if column not in transformed.columns
    ]

    if missing_output_columns:
        raise ValueError(
            "Missing calculated columns: "
            + ", ".join(missing_output_columns)
        )

    # Check for negative net amounts.
    negative_net_amounts = int(
        (transformed["net_amount"] < 0).sum()
    )

    if negative_net_amounts > 0:
        raise ValueError(
            "Negative net amounts detected: "
            f"{negative_net_amounts}"
        )

    # ---------------------------------------------------------------
    # Final logging
    # ---------------------------------------------------------------

    logger.info(
        "Transform completed successfully: "
        "%s rows, %s columns.",
        len(transformed),
        len(transformed.columns),
    )

    logger.info(
        "Customers: %s",
        transformed["customer_id"].nunique(),
    )

    logger.info(
        "Products: %s",
        transformed["product_id"].nunique(),
    )

    logger.info(
        "Total quantity: %s",
        int(transformed["quantity"].sum()),
    )

    logger.info(
        "Business revenue: %.2f",
        financial_results[
            "calculated_business_revenue"
        ],
    )

    print(
        f"TRANSFORM: {len(transformed):,} rows, "
        f"{len(transformed.columns)} columns"
    )

    return transformed
