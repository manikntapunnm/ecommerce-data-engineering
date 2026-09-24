import csv
import random
import os
from datetime import date, timedelta

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

random.seed(123)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Correct file location
OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "ecommerce.csv"
)

# Add 2,000 new rows
NEW_ROWS = 2000

# Existing rows: 1 - 10000
# New rows:      10001 - 12000
START_ORDER_ID = 10001
END_ORDER_ID = START_ORDER_ID + NEW_ROWS

# --------------------------------------------------
# CUSTOMERS
# --------------------------------------------------

customers = [
    (1001, "Rahul Kumar", "Hyderabad", "Telangana"),
    (1002, "Priya Sharma", "Bengaluru", "Karnataka"),
    (1003, "Arjun Reddy", "Vijayawada", "Andhra Pradesh"),
    (1004, "Sneha Patel", "Mumbai", "Maharashtra"),
    (1005, "Vikram Singh", "Delhi", "Delhi"),
    (1006, "Ananya Rao", "Chennai", "Tamil Nadu"),
    (1007, "Kiran Kumar", "Pune", "Maharashtra"),
    (1008, "Neha Gupta", "Kolkata", "West Bengal"),
    (1009, "Suresh Babu", "Coimbatore", "Tamil Nadu"),
    (1010, "Divya Reddy", "Warangal", "Telangana"),
    (1011, "Amit Verma", "Jaipur", "Rajasthan"),
    (1012, "Pooja Mehta", "Ahmedabad", "Gujarat"),
    (1013, "Ravi Teja", "Guntur", "Andhra Pradesh"),
    (1014, "Kavya Nair", "Kochi", "Kerala"),
    (1015, "Manoj Das", "Bhubaneswar", "Odisha"),
    (1016, "Swathi Rao", "Mysuru", "Karnataka"),
    (1017, "Naveen Reddy", "Nizamabad", "Telangana"),
    (1018, "Meena Iyer", "Madurai", "Tamil Nadu"),
    (1019, "Rohit Jain", "Surat", "Gujarat"),
    (1020, "Lakshmi Devi", "Visakhapatnam", "Andhra Pradesh"),
]

# --------------------------------------------------
# PRODUCTS
# --------------------------------------------------

products = [
    (2001, "Laptop", "Electronics", 55000, 85000),
    (2002, "Smartphone", "Electronics", 15000, 75000),
    (2003, "Headphones", "Electronics", 1000, 8000),
    (2004, "Bluetooth Speaker", "Electronics", 1500, 10000),
    (2005, "Smart Watch", "Electronics", 2500, 15000),
    (2006, "Keyboard", "Electronics", 800, 5000),
    (2007, "Mouse", "Electronics", 400, 3000),
    (2008, "Monitor", "Electronics", 8000, 35000),
    (2009, "Tablet", "Electronics", 12000, 45000),
    (2010, "Power Bank", "Electronics", 700, 4000),

    (2011, "Office Chair", "Furniture", 5000, 18000),
    (2012, "Study Table", "Furniture", 4000, 15000),
    (2013, "Bookshelf", "Furniture", 3500, 12000),
    (2014, "Sofa", "Furniture", 25000, 80000),
    (2015, "Dining Table", "Furniture", 15000, 50000),

    (2016, "Running Shoes", "Fashion", 2000, 9000),
    (2017, "T-Shirt", "Fashion", 500, 2500),
    (2018, "Jeans", "Fashion", 1200, 4500),
    (2019, "Jacket", "Fashion", 2000, 8000),
    (2020, "Backpack", "Fashion", 800, 4000),

    (2021, "Coffee Maker", "Home Appliances", 3000, 15000),
    (2022, "Mixer Grinder", "Home Appliances", 2500, 10000),
    (2023, "Air Fryer", "Home Appliances", 4000, 14000),
    (2024, "Electric Kettle", "Home Appliances", 1000, 5000),
    (2025, "Vacuum Cleaner", "Home Appliances", 5000, 20000),

    (2026, "Face Wash", "Beauty", 200, 800),
    (2027, "Shampoo", "Beauty", 300, 1200),
    (2028, "Perfume", "Beauty", 1000, 6000),
    (2029, "Moisturizer", "Beauty", 300, 1800),
    (2030, "Sunscreen", "Beauty", 300, 1500),
]

# --------------------------------------------------
# PAYMENT METHODS
# --------------------------------------------------

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery",
]

# --------------------------------------------------
# DATE RANGE
# --------------------------------------------------

start_date = date(2025, 1, 1)
end_date = date(2025, 12, 31)

date_range = (end_date - start_date).days

# --------------------------------------------------
# CHECK FILE
# --------------------------------------------------

if not os.path.exists(OUTPUT_FILE):
    print("ERROR: ecommerce.csv not found!")
    print(f"Expected location:")
    print(OUTPUT_FILE)
    exit()

# --------------------------------------------------
# APPEND 2,000 ROWS
# --------------------------------------------------

with open(
    OUTPUT_FILE,
    "a",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    for order_id in range(START_ORDER_ID, END_ORDER_ID):

        # -----------------------------
        # Random customer
        # -----------------------------

        customer = random.choice(customers)

        customer_id = customer[0]
        customer_name = customer[1]
        city = customer[2]
        state = customer[3]

        # -----------------------------
        # Random product
        # -----------------------------

        product = random.choice(products)

        product_id = product[0]
        product_name = product[1]
        category = product[2]

        # -----------------------------
        # Random unit price
        # -----------------------------

        unit_price = round(
            random.uniform(
                product[3],
                product[4]
            ),
            2
        )

        # -----------------------------
        # Random quantity
        # -----------------------------

        quantity = random.choices(
            [1, 2, 3, 4, 5],
            weights=[50, 30, 12, 5, 3],
            k=1
        )[0]

        # -----------------------------
        # Random discount
        # -----------------------------

        discount = random.choices(
            [0, 5, 10, 15, 20, 25],
            weights=[25, 25, 20, 15, 10, 5],
            k=1
        )[0]

        # -----------------------------
        # Random order date
        # -----------------------------

        order_date = start_date + timedelta(
            days=random.randint(
                0,
                date_range
            )
        )

        # -----------------------------
        # Random payment method
        # -----------------------------

        payment_method = random.choice(
            payment_methods
        )

        # -----------------------------
        # Write row
        # -----------------------------

        writer.writerow([
            order_id,
            order_date,
            customer_id,
            customer_name,
            product_id,
            product_name,
            category,
            quantity,
            unit_price,
            discount,
            city,
            state,
            "India",
            payment_method,
        ])

# --------------------------------------------------
# SUCCESS
# --------------------------------------------------

print("=" * 60)
print("SUCCESS!")
print("=" * 60)
print(f"Added rows       : {NEW_ROWS}")
print(f"Order IDs        : {START_ORDER_ID} - {END_ORDER_ID - 1}")
print(f"File updated     : {OUTPUT_FILE}")
print()
print("Total expected rows:")
print("10,000 existing + 2,000 new = 12,000 rows")
print("=" * 60)