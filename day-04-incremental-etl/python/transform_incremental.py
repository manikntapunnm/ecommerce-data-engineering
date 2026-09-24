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
]


def transform_incremental_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the Day 2/Day 3 business transformations
    to the incremental records.

    The original input DataFrame is not modified.
    """

    if df.empty:
        transformed_df = df.copy()

        transformed_df["gross_amount"] = pd.Series(
            dtype="float64"
        )
        transformed_df["discount_amount"] = pd.Series(
            dtype="float64"
        )
        transformed_df["net_amount"] = pd.Series(
            dtype="float64"
        )

        return transformed_df

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    transformed_df = df.copy()

    transformed_df["gross_amount"] = (
        transformed_df["quantity"]
        * transformed_df["unit_price"]
    )

    transformed_df["discount_amount"] = (
        transformed_df["gross_amount"]
        * transformed_df["discount"]
        / 100.0
    )

    transformed_df["net_amount"] = (
        transformed_df["gross_amount"]
        - transformed_df["discount_amount"]
    )

    return transformed_df


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]

    source_path = project_root / "data" / "raw" / "ecommerce.csv"
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
        watermark_path.read_text(encoding="utf-8").strip()
    )

    df = pd.read_csv(source_path)

    incremental_df = (
        df[df["order_id"] > watermark]
        .copy()
        .sort_values("order_id")
        .reset_index(drop=True)
    )

    transformed_df = transform_incremental_data(
        incremental_df
    )

    print(f"Watermark: {watermark}")
    print(f"Rows extracted: {len(incremental_df)}")
    print(f"Rows transformed: {len(transformed_df)}")
    print(f"Columns after transformation: {len(transformed_df.columns)}")

    if not transformed_df.empty:
        incremental_revenue = (
            transformed_df["quantity"]
            * transformed_df["unit_price"]
            * (
                1
                - transformed_df["discount"] / 100.0
            )
        ).sum()

        print(
            f"Incremental business revenue: "
            f"{incremental_revenue:.2f}"
        )

        print(
            f"First order_id: "
            f"{transformed_df['order_id'].min()}"
        )

        print(
            f"Last order_id: "
            f"{transformed_df['order_id'].max()}"
        )
