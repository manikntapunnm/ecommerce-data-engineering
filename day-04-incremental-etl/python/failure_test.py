from pathlib import Path

import pandas as pd

from validate_incremental import validate_incremental_data


def main() -> None:
    """
    Demonstrate that a validation failure does not
    modify the real watermark.
    """

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

    original_watermark = int(
        watermark_path.read_text(
            encoding="utf-8"
        ).strip()
    )

    print("=" * 60)
    print("DAY 4 — CONTROLLED FAILURE TEST")
    print("=" * 60)

    print(
        f"Original watermark: {original_watermark}"
    )

    # Read the source only.
    source_df = pd.read_csv(source_path)

    # Select records that were previously processed.
    # These are used only to demonstrate validation failure.
    test_df = source_df[
        (source_df["order_id"] > 10000)
        & (source_df["order_id"] <= 10001)
    ].copy()

    print(
        f"Test rows selected: {len(test_df)}"
    )

    # Deliberately introduce an invalid business value
    # ONLY in memory. The source CSV is NOT changed.
    test_df.loc[
        test_df.index[0],
        "quantity"
    ] = 0

    print(
        "Introduced temporary invalid quantity: 0"
    )

    # Add the transformed financial columns.
    test_df["gross_amount"] = (
        test_df["quantity"]
        * test_df["unit_price"]
    )

    test_df["discount_amount"] = (
        test_df["gross_amount"]
        * test_df["discount"]
        / 100.0
    )

    test_df["net_amount"] = (
        test_df["gross_amount"]
        - test_df["discount_amount"]
    )

    print("\nRunning validation...")

    validation_results = validate_incremental_data(
        test_df
    )

    print(
        f"Validation passed: "
        f"{validation_results['validation_passed']}"
    )

    if validation_results["validation_passed"]:
        raise RuntimeError(
            "Failure test did not fail as expected."
        )

    print(
        "\nEXPECTED FAILURE CONFIRMED"
    )

    # Read the real watermark again.
    final_watermark = int(
        watermark_path.read_text(
            encoding="utf-8"
        ).strip()
    )

    print(
        f"Watermark before test: "
        f"{original_watermark}"
    )

    print(
        f"Watermark after test:  "
        f"{final_watermark}"
    )

    if final_watermark != original_watermark:
        raise RuntimeError(
            "FAILURE: watermark changed during "
            "the controlled failure test."
        )

    print(
        "\nWatermark remained unchanged."
    )

    print(
        "Original source data was not modified."
    )

    print(
        "Controlled failure test PASSED."
    )


if __name__ == "__main__":
    main()
