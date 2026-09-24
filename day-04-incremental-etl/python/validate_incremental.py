from pathlib import Path

import pandas as pd


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


def validate_required_columns(df: pd.DataFrame) -> list[str]:
    """Return any required columns missing from the DataFrame."""
    return [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]


def validate_missing_values(df: pd.DataFrame) -> int:
    """Return the total number of missing values."""
    return int(df.isna().sum().sum())


def validate_duplicate_order_ids(df: pd.DataFrame) -> int:
    """Return the number of duplicate order ID rows."""
    return int(df["order_id"].duplicated().sum())


def validate_business_rules(df: pd.DataFrame) -> dict[str, int]:
    """
    Validate the core business rules used in Days 1–3.
    """

    invalid_order_ids = int(
        (df["order_id"] <= 0).sum()
    )

    invalid_customer_ids = int(
        (df["customer_id"] <= 0).sum()
    )

    invalid_product_ids = int(
        (df["product_id"] <= 0).sum()
    )

    invalid_quantities = int(
        (df["quantity"] <= 0).sum()
    )

    invalid_unit_prices = int(
        (df["unit_price"] < 0).sum()
    )

    invalid_discounts = int(
        (
            (df["discount"] < 0)
            | (df["discount"] > 100)
        ).sum()
    )

    invalid_dates = int(
        pd.to_datetime(
            df["order_date"],
            errors="coerce",
        ).isna().sum()
    )

    return {
        "invalid_order_ids": invalid_order_ids,
        "invalid_customer_ids": invalid_customer_ids,
        "invalid_product_ids": invalid_product_ids,
        "invalid_quantities": invalid_quantities,
        "invalid_unit_prices": invalid_unit_prices,
        "invalid_discounts": invalid_discounts,
        "invalid_dates": invalid_dates,
    }


def validate_financial_calculations(
    df: pd.DataFrame,
    tolerance: float = 0.000001,
) -> dict[str, int]:
    """
    Validate the financial calculations.

    gross_amount:
        quantity * unit_price

    discount_amount:
        gross_amount * discount / 100

    net_amount:
        gross_amount - discount_amount

    The authoritative business revenue is independently
    calculated from quantity, unit_price, and discount.
    """

    expected_gross = (
        df["quantity"]
        * df["unit_price"]
    )

    expected_discount = (
        expected_gross
        * df["discount"]
        / 100.0
    )

    expected_net = (
        expected_gross
        - expected_discount
    )

    incorrect_gross = int(
        (
            (df["gross_amount"] - expected_gross)
            .abs()
            > tolerance
        ).sum()
    )

    incorrect_discount = int(
        (
            (df["discount_amount"] - expected_discount)
            .abs()
            > tolerance
        ).sum()
    )

    incorrect_net = int(
        (
            (df["net_amount"] - expected_net)
            .abs()
            > tolerance
        ).sum()
    )

    return {
        "incorrect_gross_amounts": incorrect_gross,
        "incorrect_discount_amounts": incorrect_discount,
        "incorrect_net_amounts": incorrect_net,
    }


def calculate_incremental_revenue(
    df: pd.DataFrame,
) -> float:
    """Calculate authoritative business revenue."""
    revenue = (
        df["quantity"]
        * df["unit_price"]
        * (
            1
            - df["discount"] / 100.0
        )
    ).sum()

    return float(revenue)


def validate_incremental_data(
    df: pd.DataFrame,
) -> dict:
    """Run all incremental validation checks."""

    missing_columns = validate_required_columns(df)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    missing_values = validate_missing_values(df)

    duplicate_order_ids = validate_duplicate_order_ids(df)

    business_rules = validate_business_rules(df)

    financial_checks = validate_financial_calculations(df)

    incremental_revenue = calculate_incremental_revenue(df)

    business_rule_errors = sum(
        business_rules.values()
    )

    financial_errors = sum(
        financial_checks.values()
    )

    validation_passed = (
        len(missing_columns) == 0
        and missing_values == 0
        and duplicate_order_ids == 0
        and business_rule_errors == 0
        and financial_errors == 0
    )

    return {
        "rows_validated": len(df),
        "missing_columns": len(missing_columns),
        "missing_values": missing_values,
        "duplicate_order_ids": duplicate_order_ids,
        "invalid_business_values": business_rule_errors,
        "incorrect_financial_values": financial_errors,
        "incremental_revenue": incremental_revenue,
        "validation_passed": validation_passed,
        **business_rules,
        **financial_checks,
    }


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]

    source_path = (
        project_root
        / "data"
        / "raw"
        / "ecommerce.csv"
    )

    watermark_path = (
        project_root
        / "day-04-incremental-etl"
        / "state"
        / "watermark.txt"
    )

    if not source_path.exists():
        raise FileNotFoundError(
            f"Source file not found: {source_path}"
        )

    if not watermark_path.exists():
        raise FileNotFoundError(
            f"Watermark file not found: {watermark_path}"
        )

    watermark = int(
        watermark_path.read_text(
            encoding="utf-8"
        ).strip()
    )

    source_df = pd.read_csv(source_path)

    incremental_df = (
        source_df[
            source_df["order_id"] > watermark
        ]
        .copy()
        .sort_values("order_id")
        .reset_index(drop=True)
    )

    # Apply the same transformation logic used
    # by the Day 4 transformation stage.
    incremental_df["gross_amount"] = (
        incremental_df["quantity"]
        * incremental_df["unit_price"]
    )

    incremental_df["discount_amount"] = (
        incremental_df["gross_amount"]
        * incremental_df["discount"]
        / 100.0
    )

    incremental_df["net_amount"] = (
        incremental_df["gross_amount"]
        - incremental_df["discount_amount"]
    )

    results = validate_incremental_data(
        incremental_df
    )

    print(f"Watermark: {watermark}")
    print(
        f"Rows being validated: "
        f"{results['rows_validated']}"
    )
    print(
        f"Missing columns: "
        f"{results['missing_columns']}"
    )
    print(
        f"Missing values: "
        f"{results['missing_values']}"
    )
    print(
        f"Duplicate order IDs: "
        f"{results['duplicate_order_ids']}"
    )
    print(
        f"Invalid business values: "
        f"{results['invalid_business_values']}"
    )
    print(
        f"Incorrect financial values: "
        f"{results['incorrect_financial_values']}"
    )
    print(
        f"Incremental revenue: "
        f"{results['incremental_revenue']:.2f}"
    )
    print(
        f"Validation passed: "
        f"{results['validation_passed']}"
    )
