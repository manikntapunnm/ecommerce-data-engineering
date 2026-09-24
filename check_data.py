import csv

file_path = "data/raw/ecommerce.csv"

with open(file_path, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    rows = list(reader)

print("Total rows including header:", len(rows))
print("Data rows:", len(rows) - 1)

if len(rows) > 1:
    print("First order ID:", rows[1][0])
    print("Last order ID:", rows[-1][0])

if len(rows) - 1 == 12000:
    print("✅ Correct! You have 12,000 data rows.")
else:
    print("⚠️ Row count is not 12,000.")

