"""
Day 2 - Revenue Diagnostic

This script compares the raw dataset and cleaned dataset
to determine why the Day 2 net revenue differs from the
Day 1 PostgreSQL revenue.
"""

from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "ecommerce.csv"
)

CLEAN_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ecommerce_clean.csv"
)


# ---------------------------------------------------------------------------
# Load datasets
# ---------------------------------------------------------------------------

print("=" * 70)
print("DAY 2 - REVENUE DIAGNOSTIC")
print("=" * 70)

print("\nLoading raw dataset...")
raw_df = pd.read_csv(RAW_DATA_PATH)

print("Loading cleaned dataset...")
clean_df = pd.read_csv(CLEAN_DATA_PATH)


# ---------------------------------------------------------------------------
# Calculate revenue directly from raw data
# ---------------------------------------------------------------------------

raw_revenue = (
    raw_df["quantity"]
    * raw_df["unit_price"]
    * (1 - raw_df["discount"] / 100.0)
).sum()


# ---------------------------------------------------------------------------
# Calculate revenue using the alternative mathematical form
# ---------------------------------------------------------------------------

raw_gross = (
    raw_df["quantity"]
    * raw_df["unit_price"]
)

raw_discount = (
    raw_gross
    * raw_df["discount"]
    / 100.0
)

raw_net_alternative = (
    raw_gross
    - raw_discount
).sum()


# ---------------------------------------------------------------------------
# Calculate revenue from cleaned data
# ---------------------------------------------------------------------------

clean_revenue = clean_df["net_amount"].sum()


# ---------------------------------------------------------------------------
# Display totals
# ---------------------------------------------------------------------------

print("\nRevenue calculations")
print("-" * 70)

print(f"Raw direct formula       : {raw_revenue:,.10f}")
print(f"Raw gross-discount form  : {raw_net_alternative:,.10f}")
print(f"Cleaned net_amount       : {clean_revenue:,.10f}")

print("\nRounded values")
print("-" * 70)

print(f"Raw direct formula       : {raw_revenue:,.2f}")
print(f"Raw gross-discount form  : {raw_net_alternative:,.2f}")
print(f"Cleaned net_amount       : {clean_revenue:,.2f}")

print("\nDifferences")
print("-" * 70)

print(
    f"Raw formula difference   : "
    f"{raw_revenue - raw_net_alternative:,.10f}"
)

print(
    f"Raw vs cleaned difference: "
    f"{raw_revenue - clean_revenue:,.10f}"
)


# ---------------------------------------------------------------------------
# Check individual rows
# ---------------------------------------------------------------------------

raw_calculated_net = (
    raw_df["quantity"]
    * raw_df["unit_price"]
    * (1 - raw_df["discount"] / 100.0)
)

clean_calculated_net = clean_df["net_amount"]

row_difference = (
    raw_calculated_net
    - clean_calculated_net
).abs()

print("\nRow-level comparison")
print("-" * 70)

print(
    f"Rows with difference > 0.000001: "
    f"{(row_difference > 0.000001).sum():,}"
)

print(
    f"Maximum row difference: "
    f"{row_difference.max():,.10f}"
)

print(
    f"Total absolute row difference: "
    f"{row_difference.sum():,.10f}"
)


# ---------------------------------------------------------------------------
# Show largest differences
# ---------------------------------------------------------------------------

if (row_difference > 0.000001).any():

    comparison = pd.DataFrame(
        {
            "order_id": raw_df["order_id"],
            "raw_calculated_net": raw_calculated_net,
            "cleaned_net_amount": clean_calculated_net,
            "absolute_difference": row_difference,
        }
    )

    comparison = comparison.sort_values(
        "absolute_difference",
        ascending=False,
    )

    print("\nLargest row-level differences")
    print("-" * 70)

    print(
        comparison.head(10).to_string(index=False)
    )


# ---------------------------------------------------------------------------
# Final message
# ---------------------------------------------------------------------------

print("\n" + "=" * 70)
print("REVENUE DIAGNOSTIC COMPLETED")
print("=" * 70)