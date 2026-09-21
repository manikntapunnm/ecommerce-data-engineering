"""
Day 2 - Revenue Validation

Validates that the cleaned dataset produces the same aggregate
business revenue as the original raw dataset.

Important:
The comparison uses the original business formula before
transaction-level currency rounding.
"""

from pathlib import Path

import pandas as pd


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


EXPECTED_DAY_1_REVENUE = 214_366_057.77


# ---------------------------------------------------------------------------
# Load datasets
# ---------------------------------------------------------------------------

if not RAW_DATA_PATH.exists():
    raise FileNotFoundError(
        f"Raw dataset not found:\n{RAW_DATA_PATH}"
    )

if not CLEAN_DATA_PATH.exists():
    raise FileNotFoundError(
        f"Cleaned dataset not found:\n{CLEAN_DATA_PATH}"
    )


raw_df = pd.read_csv(RAW_DATA_PATH)
clean_df = pd.read_csv(CLEAN_DATA_PATH)


# ---------------------------------------------------------------------------
# Calculate revenue from the raw business formula
# ---------------------------------------------------------------------------

raw_revenue = (
    raw_df["quantity"]
    * raw_df["unit_price"]
    * (1 - raw_df["discount"] / 100.0)
).sum()


# ---------------------------------------------------------------------------
# Calculate the same business formula using cleaned columns
# ---------------------------------------------------------------------------

clean_formula_revenue = (
    clean_df["quantity"]
    * clean_df["unit_price"]
    * (1 - clean_df["discount"] / 100.0)
).sum()


# ---------------------------------------------------------------------------
# Transaction-level revenue
# ---------------------------------------------------------------------------

transaction_revenue = clean_df["net_amount"].sum()


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

print("=" * 70)
print("DAY 2 REVENUE VALIDATION")
print("=" * 70)

print(f"\nRows in raw dataset   : {len(raw_df):,}")
print(f"Rows in clean dataset : {len(clean_df):,}")

print("\nRevenue calculations")
print("-" * 70)

print(f"Raw business formula       : {raw_revenue:,.2f}")
print(f"Clean business formula     : {clean_formula_revenue:,.2f}")
print(f"Rounded transaction total  : {transaction_revenue:,.2f}")

print("\nDay 1 reference")
print("-" * 70)

print(f"Expected Day 1 revenue     : {EXPECTED_DAY_1_REVENUE:,.2f}")

raw_difference = (
    raw_revenue - EXPECTED_DAY_1_REVENUE
)

clean_formula_difference = (
    clean_formula_revenue - EXPECTED_DAY_1_REVENUE
)

transaction_rounding_difference = (
    transaction_revenue - clean_formula_revenue
)

print("\nDifferences")
print("-" * 70)

print(
    f"Raw vs Day 1               : "
    f"{raw_difference:,.2f}"
)

print(
    f"Clean formula vs Day 1     : "
    f"{clean_formula_difference:,.2f}"
)

print(
    f"Transaction rounding diff  : "
    f"{transaction_rounding_difference:,.2f}"
)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

print("\nValidation results")
print("-" * 70)

if abs(raw_difference) < 0.01:
    print("PASS - Raw dataset matches Day 1 revenue.")
else:
    print("FAIL - Raw dataset does not match Day 1 revenue.")

if abs(clean_formula_difference) < 0.01:
    print("PASS - Clean dataset preserves Day 1 revenue calculation.")
else:
    print("FAIL - Clean dataset changes the Day 1 revenue calculation.")


print("\n" + "=" * 70)
print("REVENUE VALIDATION COMPLETED")
print("=" * 70)