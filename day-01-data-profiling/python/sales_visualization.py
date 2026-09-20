import pandas as pd  # type: ignore[reportMissingModuleSource]
import matplotlib.pyplot as plt  # type: ignore[reportMissingModuleSource]
import seaborn as sns  # type: ignore[reportMissingModuleSource]
import os

# ---------------------------------------------------------
# E-COMMERCE SALES VISUALIZATION
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

# Calculate revenue
df["revenue"] = (
    df["quantity"]
    * df["unit_price"]
    * (1 - df["discount"] / 100)
)

# ---------------------------------------------------------
# Revenue by State
# ---------------------------------------------------------

state_revenue = (
    df.groupby("state")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12, 6))

sns.barplot(
    x=state_revenue.values,
    y=state_revenue.index,
    color="steelblue"
)

plt.title("Revenue by State")
plt.xlabel("Revenue")
plt.ylabel("State")

plt.tight_layout()

output_file = os.path.join(
    OUTPUT_DIR,
    "sales_distribution.png"
)

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Visualization created successfully:")
print(output_file)
