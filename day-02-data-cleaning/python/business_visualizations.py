"""
Day 2 - Business Visualizations

Creates visual evidence from the cleaned e-commerce dataset.

Outputs:
1. Revenue by category
2. Monthly revenue
3. Payment method revenue
4. State revenue
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLEAN_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ecommerce_clean.csv"
)

SCREENSHOTS_DIR = (
    PROJECT_ROOT
    / "day-02-data-cleaning"
    / "screenshots"
)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

sns.set_theme(style="whitegrid")

SCREENSHOTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

def load_clean_data() -> pd.DataFrame:
    """Load the cleaned e-commerce dataset."""

    if not CLEAN_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Clean dataset was not found:\n{CLEAN_DATA_PATH}"
        )

    dataframe = pd.read_csv(CLEAN_DATA_PATH)

    dataframe["order_date"] = pd.to_datetime(
        dataframe["order_date"],
        errors="raise",
    )

    return dataframe


# ---------------------------------------------------------------------------
# Revenue by category
# ---------------------------------------------------------------------------

def create_category_revenue_chart(dataframe: pd.DataFrame) -> None:
    """Create revenue by category chart."""

    category_revenue = (
        dataframe.groupby("category", as_index=False)["net_amount"]
        .sum()
        .sort_values("net_amount", ascending=False)
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=category_revenue,
        x="net_amount",
        y="category",
        color="steelblue",
    )

    plt.title("Day 2 - Net Revenue by Category")
    plt.xlabel("Net Revenue")
    plt.ylabel("Category")

    plt.tight_layout()

    output_path = (
        SCREENSHOTS_DIR
        / "category_revenue.png"
    )

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Created: {output_path}")


# ---------------------------------------------------------------------------
# Monthly revenue
# ---------------------------------------------------------------------------

def create_monthly_revenue_chart(dataframe: pd.DataFrame) -> None:
    """Create monthly revenue chart."""

    dataframe = dataframe.copy()

    dataframe["month"] = dataframe["order_date"].dt.to_period("M").astype(str)

    monthly_revenue = (
        dataframe.groupby("month", as_index=False)["net_amount"]
        .sum()
    )

    plt.figure(figsize=(12, 6))

    sns.lineplot(
        data=monthly_revenue,
        x="month",
        y="net_amount",
        marker="o",
        color="darkgreen",
    )

    plt.title("Day 2 - Monthly Net Revenue")
    plt.xlabel("Month")
    plt.ylabel("Net Revenue")

    plt.xticks(rotation=45)

    plt.tight_layout()

    output_path = (
        SCREENSHOTS_DIR
        / "monthly_revenue.png"
    )

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Created: {output_path}")


# ---------------------------------------------------------------------------
# Payment method revenue
# ---------------------------------------------------------------------------

def create_payment_method_chart(dataframe: pd.DataFrame) -> None:
    """Create payment-method revenue chart."""

    payment_revenue = (
        dataframe.groupby(
            "payment_method",
            as_index=False,
        )["net_amount"]
        .sum()
        .sort_values("net_amount", ascending=False)
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=payment_revenue,
        x="net_amount",
        y="payment_method",
        color="darkorange",
    )

    plt.title("Day 2 - Net Revenue by Payment Method")
    plt.xlabel("Net Revenue")
    plt.ylabel("Payment Method")

    plt.tight_layout()

    output_path = (
        SCREENSHOTS_DIR
        / "payment_method_revenue.png"
    )

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Created: {output_path}")


# ---------------------------------------------------------------------------
# State revenue
# ---------------------------------------------------------------------------

def create_state_revenue_chart(dataframe: pd.DataFrame) -> None:
    """Create revenue by state chart."""

    state_revenue = (
        dataframe.groupby("state", as_index=False)["net_amount"]
        .sum()
        .sort_values("net_amount", ascending=False)
    )

    plt.figure(figsize=(11, 7))

    sns.barplot(
        data=state_revenue,
        x="net_amount",
        y="state",
        color="mediumpurple",
    )

    plt.title("Day 2 - Net Revenue by State")
    plt.xlabel("Net Revenue")
    plt.ylabel("State")

    plt.tight_layout()

    output_path = (
        SCREENSHOTS_DIR
        / "state_revenue.png"
    )

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Created: {output_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Run all Day 2 visualizations."""

    print("=" * 70)
    print("DAY 2 - BUSINESS VISUALIZATIONS")
    print("=" * 70)

    print("\nLoading cleaned dataset...")

    dataframe = load_clean_data()

    print(f"Rows loaded: {len(dataframe):,}")
    print(f"Columns loaded: {len(dataframe.columns)}")

    print("\nCreating visualizations...")

    create_category_revenue_chart(dataframe)
    create_monthly_revenue_chart(dataframe)
    create_payment_method_chart(dataframe)
    create_state_revenue_chart(dataframe)

    print("\n" + "=" * 70)
    print("DAY 2 VISUALIZATIONS COMPLETED")
    print("=" * 70)

    print(f"\nScreenshots directory:")
    print(SCREENSHOTS_DIR)


if __name__ == "__main__":
    main()
