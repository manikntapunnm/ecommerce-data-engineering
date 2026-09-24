from pathlib import Path

import pandas as pd


def read_watermark(watermark_path: Path) -> int:
    """
    Read the last successfully processed order_id.

    The watermark represents the latest record that the pipeline
    successfully processed during a previous run.
    """
    if not watermark_path.exists():
        raise FileNotFoundError(
            f"Watermark file not found: {watermark_path}"
        )

    watermark_text = watermark_path.read_text(encoding="utf-8").strip()

    if not watermark_text:
        raise ValueError("Watermark file is empty.")

    try:
        watermark = int(watermark_text)
    except ValueError as exc:
        raise ValueError(
            f"Watermark must contain a valid integer. "
            f"Found: {watermark_text!r}"
        ) from exc

    if watermark < 0:
        raise ValueError(
            f"Watermark cannot be negative. Found: {watermark}"
        )

    return watermark


def extract_incremental_data(
    source_path: Path,
    watermark_path: Path,
) -> tuple[pd.DataFrame, int]:
    """
    Read the source CSV and return only records newer than the watermark.

    Returns:
        A tuple containing:
        - DataFrame containing new records
        - Watermark value used for extraction
    """
    if not source_path.exists():
        raise FileNotFoundError(
            f"Source file not found: {source_path}"
        )

    watermark = read_watermark(watermark_path)

    df = pd.read_csv(source_path)

    if "order_id" not in df.columns:
        raise ValueError(
            "Required column 'order_id' is missing from the source file."
        )

    if df["order_id"].isna().any():
        raise ValueError(
            "Source contains missing order_id values."
        )

    new_records = (
        df[df["order_id"] > watermark]
        .copy()
        .sort_values("order_id")
        .reset_index(drop=True)
    )

    return new_records, watermark


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]

    source_path = project_root / "data" / "raw" / "ecommerce.csv"
    watermark_path = (
        project_root
        / "day-04-incremental-etl"
        / "state"
        / "watermark.txt"
    )

    new_data, watermark = extract_incremental_data(
        source_path,
        watermark_path,
    )

    print(f"Watermark: {watermark}")
    print(f"Source rows: {pd.read_csv(source_path).shape[0]}")
    print(f"Incremental rows: {len(new_data)}")

    if not new_data.empty:
        print(f"First new order_id: {new_data['order_id'].min()}")
        print(f"Last new order_id: {new_data['order_id'].max()}")
    else:
        print("No new records found.")

# Remove-Item "day-04-incremental-etl\output\ecommerce_incremental_load.csv"
