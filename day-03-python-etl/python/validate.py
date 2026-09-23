"""
Day 3 - Python ETL Pipeline
Validation Stage

Responsible for validating the transformed dataset before loading.

Validation includes:
    - Required columns
    - Row count
    - Missing values
    - Duplicate order IDs
    - Business rules
    - Financial calculations
    - Revenue reconciliation
"""

import logging

import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# Expected Day 1 reference values
# -------------------------------------------------------------------

EXPECTED_BUSINESS_REVENUE = 214366057.77
EXPECTED_ROW_COUNT = 10000
EXPECTED_CUSTOMER_COUNT = 20
EXPECTED_PRODUCT_COUNT = 30
EXPECTED_TOTAL_QUANTITY = 18154


# -------------------------------------------------------------------
# Required columns
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
    "gross_amount",
    "discount_amount",
    "net_amount",
]


# -------------------------------------------------------------------
# Required column validation
# -------------------------------------------------------------------

def validate_required_columns(
    dataframe: pd.DataFrame,
) -> None:
    """
    Verify that all expected columns exist.
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

    logger.info(
        "Required-column validation passed."
    )


# -------------------------------------------------------------------
# Row-count validation
# -------------------------------------------------------------------

def validate_row_count(
    dataframe: pd.DataFrame,
) -> None:
    """
    Verify the expected number of rows.
    """

    row_count = len(dataframe)

    if row_count != EXPECTED_ROW_COUNT:
        raise ValueError(
            f"Unexpected row count: {row_count}. "
            f"Expected {EXPECTED_ROW_COUNT}."
        )

    logger.info(
        "Row-count validation passed: %s rows.",
        row_count,
    )


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
        Total missing values.
    """

    missing_values = int(
        dataframe.isna().sum().sum()
    )

    if missing_values > 0:
        raise ValueError(
            f"Validation failed: "
            f"{missing_values} missing values detected."
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
# Customer validation
# -------------------------------------------------------------------

def get_customer_count(
    dataframe: pd.DataFrame,
) -> int:
    """
    Return the number of unique customers.
    """

    customer_count = int(
        dataframe["customer_id"].nunique()
    )

    if customer_count != EXPECTED_CUSTOMER_COUNT:
        raise ValueError(
            f"Unexpected customer count: "
            f"{customer_count}. "
            f"Expected {EXPECTED_CUSTOMER_COUNT}."
        )

    return customer_count


# -------------------------------------------------------------------
# Product validation
# -------------------------------------------------------------------

def get_product_count(
    dataframe: pd.DataFrame,
) -> int:
    """
    Return the number of unique products.
    """

    product_count = int(
        dataframe["product_id"].nunique()
    )

    if product_count != EXPECTED_PRODUCT_COUNT:
        raise ValueError(
            f"Unexpected product count: "
            f"{product_count}. "
            f"Expected {EXPECTED_PRODUCT_COUNT}."
        )

    return product_count


# -------------------------------------------------------------------
# Quantity validation
# -------------------------------------------------------------------

def get_total_quantity(
    dataframe: pd.DataFrame,
) -> int:
    """
    Return total quantity.
    """

    total_quantity = int(
        dataframe["quantity"].sum()
    )

    if total_quantity != EXPECTED_TOTAL_QUANTITY:
        raise ValueError(
            f"Unexpected total quantity: "
            f"{total_quantity}. "
            f"Expected {EXPECTED_TOTAL_QUANTITY}."
        )

    return total_quantity


# -------------------------------------------------------------------
# Financial validation
# -------------------------------------------------------------------

def validate_financial_calculations(
    dataframe: pd.DataFrame,
) -> dict:
    """
    Validate calculated financial columns.

    IMPORTANT:
    The validation reproduces the exact calculation sequence
    used in transform.py.

    Raw calculation:

        gross_raw =
            quantity * unit_price

        discount_raw =
            gross_raw * discount / 100

        net_raw =
            gross_raw - discount_raw

    Stored values are rounded to two decimals.
    """

    # ---------------------------------------------------------------
    # Recreate raw calculations.
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
    # Expected stored values.
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
    # Compare stored values.
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
    # Report financial calculation errors.
    # ---------------------------------------------------------------

    if incorrect_gross > 0:
        raise ValueError(
            "Validation failed: "
            f"{incorrect_gross} incorrect gross calculations."
        )

    if incorrect_discount > 0:
        raise ValueError(
            "Validation failed: "
            f"{incorrect_discount} incorrect discount "
            "calculations."
        )

    if incorrect_net > 0:
        raise ValueError(
            "Validation failed: "
            f"{incorrect_net} incorrect net calculations."
        )

    # ---------------------------------------------------------------
    # Day 1 business revenue reconciliation.
    #
    # This deliberately uses the original unrounded formula.
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
            f"Expected "
            f"{EXPECTED_BUSINESS_REVENUE:,.2f}, "
            f"calculated "
            f"{calculated_business_revenue:,.2f}, "
            f"difference "
            f"{revenue_difference:,.2f}"
        )

    logger.info(
        "Financial calculation validation passed."
    )

    logger.info(
        "Business revenue: %.2f",
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
# Main validation function
# -------------------------------------------------------------------

def validate_data(
    dataframe: pd.DataFrame,
) -> dict:
    """
    Execute all validation checks.

    Returns
    -------
    dict
        Validation results used by the ETL orchestrator.
    """

    logger.info(
        "Starting validation stage."
    )

    logger.info(
        "Validation input: %s rows, %s columns.",
        len(dataframe),
        len(dataframe.columns),
    )

    # ---------------------------------------------------------------
    # Required columns
    # ---------------------------------------------------------------

    validate_required_columns(
        dataframe
    )

    # ---------------------------------------------------------------
    # Row count
    # ---------------------------------------------------------------

    validate_row_count(
        dataframe
    )

    # ---------------------------------------------------------------
    # Missing values
    # ---------------------------------------------------------------

    missing_values = validate_missing_values(
        dataframe
    )

    # ---------------------------------------------------------------
    # Duplicate IDs
    # ---------------------------------------------------------------

    duplicate_order_ids = validate_duplicates(
        dataframe
    )

    # ---------------------------------------------------------------
    # Business rules
    # ---------------------------------------------------------------

    validate_business_rules(
        dataframe
    )

    # ---------------------------------------------------------------
    # Basic dataset metrics
    # ---------------------------------------------------------------

    customer_count = get_customer_count(
        dataframe
    )

    product_count = get_product_count(
        dataframe
    )

    total_quantity = get_total_quantity(
        dataframe
    )

    # ---------------------------------------------------------------
    # Financial validation
    # ---------------------------------------------------------------

    financial_results = validate_financial_calculations(
        dataframe
    )

    # ---------------------------------------------------------------
    # Final validation status
    # ---------------------------------------------------------------

    validation_status = "PASSED"

    logger.info(
        "All validation checks passed."
    )

    print(
        "VALIDATE: "
        f"{len(dataframe):,} rows passed all validations"
    )

    print(
        "VALIDATE: Revenue = "
        f"{financial_results['calculated_business_revenue']:,.2f}"
    )

    print(
        "VALIDATE: All checks passed"
    )

    return {
        "validation_status":
            validation_status,

        "customer_count":
            customer_count,

        "product_count":
            product_count,

        "total_quantity":
            total_quantity,

        "missing_values":
            missing_values,

        "duplicate_order_ids":
            duplicate_order_ids,

        "calculated_business_revenue":
            financial_results[
                "calculated_business_revenue"
            ],

        "expected_business_revenue":
            financial_results[
                "expected_business_revenue"
            ],

        "revenue_difference":
            financial_results[
                "revenue_difference"
            ],
    }
