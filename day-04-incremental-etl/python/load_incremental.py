from pathlib import Path

import pandas as pd


def load_incremental_data(
    existing_path: Path,
    incremental_df: pd.DataFrame,
) -> tuple[pd.DataFrame, int]:
    """
    Append only genuinely new records to the existing
    processed dataset.

    Duplicate order IDs already present in the target
    are skipped.

    Returns:
        Updated DataFrame and number of rows actually loaded.
    """

    if not existing_path.exists():
        raise FileNotFoundError(
            f"Existing processed file not found: {existing_path}"
        )

    existing_df = pd.read_csv(existing_path)

    if "order_id" not in existing_df.columns:
        raise ValueError(
            "Existing processed dataset is missing 'order_id'."
        )

    if "order_id" not in incremental_df.columns:
        raise ValueError(
            "Incremental dataset is missing 'order_id'."
        )

    existing_order_ids = set(
        existing_df["order_id"].astype(int)
    )

    new_records = incremental_df[
        ~incremental_df["order_id"].isin(
            existing_order_ids
        )
    ].copy()

    if new_records.empty:
        return existing_df, 0

    updated_df = pd.concat(
        [existing_df, new_records],
        ignore_index=True,
    )

    updated_df = (
        updated_df
        .sort_values("order_id")
        .reset_index(drop=True)
    )

    updated_df.to_csv(
        existing_path,
        index=False,
    )

    return updated_df, len(new_records)


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]

    processed_path = (
        project_root
        / "data"
        / "processed"
        / "ecommerce_clean.csv"
    )

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

    updated_df, rows_loaded = load_incremental_data(
        processed_path,
        incremental_df,
    )

    print(f"Watermark before load: {watermark}")
    print(f"Rows identified: {len(incremental_df)}")
    print(f"Rows actually loaded: {rows_loaded}")
    print(f"Rows in processed dataset: {len(updated_df)}")
    print(
        f"Unique order IDs: "
        f"{updated_df['order_id'].nunique()}"
    )

    print(
        "Watermark was not changed by the loader."
    )
