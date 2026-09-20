import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------------------------------------------------------
# E-COMMERCE BUSINESS VISUALIZATIONS
# Day 1
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "ecommerce.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "day-01-data-profiling",
    "screenshots"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data
df = pd.read_csv(INPUT_FILE)

# Convert date
df["order_date"] = pd.to_datetime(df["order_date"])

# Calculate revenue after discount
df["revenue"] = (
    df["quantity"]
    * df["unit_price"]
    * (1 - df["discount"] / 100)
)

sns.set_theme(style="whitegrid")


# ---------------------------------------------------------
# 1. Revenue by State
# ---------------------------------------------------------

state_revenue = (
    df.groupby("state")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12, 7))

sns.barplot(
    x=state_revenue.values,
    y=state_revenue.index,
    color="steelblue"
)

plt.title("Revenue by State")
plt.xlabel("Revenue")
plt.ylabel("State")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "sales_distribution.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# 2. Revenue by Category
# ---------------------------------------------------------

category_revenue = (
    df.groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=category_revenue.index,
    y=category_revenue.values,
    color="darkorange"
)

plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "category_revenue.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# 3. Monthly Revenue
# ---------------------------------------------------------

monthly_revenue = (
    df.groupby(
        df["order_date"].dt.to_period("M")
    )["revenue"]
    .sum()
)

monthly_revenue.index = monthly_revenue.index.astype(str)

plt.figure(figsize=(12, 6))

sns.lineplot(
    x=monthly_revenue.index,
    y=monthly_revenue.values,
    marker="o",
    color="darkgreen"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "monthly_revenue.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# Completion
# ---------------------------------------------------------

print("=" * 60)
print("BUSINESS VISUALIZATIONS CREATED SUCCESSFULLY")
print("=" * 60)

print("\nCreated files:")

print(
    os.path.join(
        OUTPUT_DIR,
        "sales_distribution.png"
    )
)

print(
    os.path.join(
        OUTPUT_DIR,
        "category_revenue.png"
    )
)

print(
    os.path.join(
        OUTPUT_DIR,
        "monthly_revenue.png"
    )
)
