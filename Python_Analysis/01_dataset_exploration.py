
# ==========================================
# BRAZILIAN E-COMMERCE MARKETPLACE ANALYSIS
# Dataset Loading and Initial Inspection
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load all datasets

customers = pd.read_csv("../Dataset/olist_customers_dataset.csv")

geolocation = pd.read_csv("../Dataset/olist_geolocation_dataset.csv")

order_items = pd.read_csv("../Dataset/olist_order_items_dataset.csv")

payments = pd.read_csv("../Dataset/olist_order_payments_dataset.csv")

reviews = pd.read_csv("../Dataset/olist_order_reviews_dataset.csv")

orders = pd.read_csv("../Dataset/olist_orders_dataset.csv")

products = pd.read_csv("../Dataset/olist_products_dataset.csv")

sellers = pd.read_csv("../Dataset/olist_sellers_dataset.csv")

category_translation = pd.read_csv(
    "../Dataset/product_category_name_translation.csv"
)

# Store datasets in one dictionary

datasets = {
    "Customers": customers,
    "Geolocation": geolocation,
    "Order Items": order_items,
    "Payments": payments,
    "Reviews": reviews,
    "Orders": orders,
    "Products": products,
    "Sellers": sellers,
    "Category Translation": category_translation
}

# Display dataset dimensions

print("\n========== DATASET OVERVIEW ==========")

for name, dataframe in datasets.items():
    print(f"{name}: {dataframe.shape[0]:,} rows, {dataframe.shape[1]} columns")

print("\nAll nine datasets loaded successfully!")



# ==========================================
# DAY 2: DATA QUALITY ASSESSMENT
# ==========================================

print("\n========== DATA QUALITY ASSESSMENT ==========")

quality_results = []

for name, df in datasets.items():

    quality_results.append({
        "Dataset": name,
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": df.isnull().sum().sum(),
        "Rows With Missing Values": df.isnull().any(axis=1).sum(),
        "Exact Duplicate Rows": df.duplicated().sum()
    })

quality_report = pd.DataFrame(quality_results)

print("\nDATA QUALITY SUMMARY")
print(quality_report.to_string(index=False))

# Save the quality report
quality_report.to_csv("data_quality_report.csv", index=False)

# ==========================================
# CHECK KEY UNIQUENESS
# ==========================================

key_checks = {
    "Customers": ["customer_id"],
    "Orders": ["order_id"],
    "Products": ["product_id"],
    "Sellers": ["seller_id"],
    "Order Items": ["order_id", "order_item_id"],
    "Payments": ["order_id", "payment_sequential"],
    "Reviews": ["review_id"],
    "Category Translation": ["product_category_name"]
}

print("\n========== KEY UNIQUENESS CHECK ==========")

for name, columns in key_checks.items():

    df = datasets[name]

    duplicate_count = df.duplicated(subset=columns).sum()

    print(
        f"{name}: {duplicate_count:,} duplicate key combinations "
        f"using {columns}"
    )

print("\nDATA QUALITY ASSESSMENT COMPLETED!")


# ==========================================
# INVESTIGATING DUPLICATE REVIEW IDs
# ==========================================

print("\n========== REVIEW DUPLICATE INVESTIGATION ==========")

# Identify records with repeated review IDs
duplicate_reviews = reviews[
    reviews.duplicated(subset=["review_id"], keep=False)
].sort_values("review_id")

print("\nTotal records with repeated review IDs:")
print(len(duplicate_reviews))

# Display the first 20 records
print("\nDUPLICATE REVIEW RECORDS:")
print(duplicate_reviews.head(20).to_string(index=False))

# Check exact duplicate rows
print("\nExact duplicate review rows:")
print(reviews.duplicated().sum())

# Count occurrences of each review ID
print("\nMost frequently repeated review IDs:")
print(reviews["review_id"].value_counts().head(10))

# Save duplicate records for investigation
duplicate_reviews.to_csv(
    "duplicate_review_investigation.csv",
    index=False
)


# ==========================================
# VALIDATING REVIEW COMPOSITE KEY
# ==========================================

print("\n========== REVIEW KEY VALIDATION ==========")

# Check whether review_id + order_id is unique
review_key_duplicates = reviews.duplicated(
    subset=["review_id", "order_id"]
).sum()

print(
    "Duplicate review_id + order_id combinations:",
    review_key_duplicates
)

# Check how many review IDs are repeated
repeated_review_ids = (
    reviews["review_id"].value_counts()
)

print(
    "Number of review IDs appearing more than once:",
    (repeated_review_ids > 1).sum()
)

# Check the number of unique review IDs
print(
    "Unique review IDs:",
    reviews["review_id"].nunique()
)

# Check the number of unique orders in reviews
print(
    "Unique order IDs in reviews:",
    reviews["order_id"].nunique()
)



# ==========================================
# MISSING VALUE ANALYSIS
# ==========================================

print("\n========== MISSING VALUE ANALYSIS ==========")

missing_results = []

for name, df in datasets.items():

    for column in df.columns:

        missing_count = df[column].isnull().sum()

        if missing_count > 0:

            missing_percentage = (
                missing_count / len(df)
            ) * 100

            missing_results.append({
                "Dataset": name,
                "Column": column,
                "Missing Count": missing_count,
                "Missing Percentage": round(missing_percentage, 2)
            })

missing_report = pd.DataFrame(missing_results)

if not missing_report.empty:

    missing_report = missing_report.sort_values(
        by="Missing Percentage",
        ascending=False
    )

    print(missing_report.to_string(index=False))

else:
    print("No missing values found.")

# Save missing value report
missing_report.to_csv(
    "missing_value_report.csv",
    index=False
)

print("\nMissing value analysis completed!")



# ==========================================
# INVESTIGATING MISSING VALUES
# ==========================================

print("\n========== ORDER DELIVERY STATUS ==========")

# Check order status for missing delivery dates
delivery_check = orders[
    orders["order_delivered_customer_date"].isnull()
]

print("\nOrder status for missing customer delivery dates:")
print(delivery_check["order_status"].value_counts(dropna=False))

print("\nOrder status for missing carrier delivery dates:")
print(
    orders[
        orders["order_delivered_carrier_date"].isnull()
    ]["order_status"].value_counts(dropna=False)
)

print("\nOrder status for missing approval dates:")
print(
    orders[
        orders["order_approved_at"].isnull()
    ]["order_status"].value_counts(dropna=False)
)

# ==========================================
# INVESTIGATING MISSING PRODUCT INFORMATION
# ==========================================

print("\n========== PRODUCT MISSING VALUE ANALYSIS ==========")

missing_products = products[
    products["product_category_name"].isnull()
]

print("\nNumber of products with missing category:")
print(len(missing_products))

print("\nMissing product information by column:")
print(missing_products.isnull().sum())

print("\nSample of products with missing categories:")
print(missing_products.head(10).to_string(index=False))

# Check whether all missing product fields occur together
print("\nMissing product field patterns:")
print(
    products[
        products["product_category_name"].isnull()
    ].isnull().sum(axis=1).value_counts().sort_index()
)


# ==========================================
# ORDER STATUS AND MISSING DELIVERY ANALYSIS
# ==========================================

print("\n========== MISSING DELIVERY DATE ANALYSIS ==========")

missing_delivery = orders[
    orders["order_delivered_customer_date"].isnull()
]

print("\nOrders with missing customer delivery dates:")
print(len(missing_delivery))

print("\nStatus breakdown:")
print(
    missing_delivery["order_status"]
    .value_counts(dropna=False)
)

print("\nMissing carrier delivery date status breakdown:")
print(
    orders[
        orders["order_delivered_carrier_date"].isnull()
    ]["order_status"].value_counts(dropna=False)
)

print("\nMissing approval date status breakdown:")
print(
    orders[
        orders["order_approved_at"].isnull()
    ]["order_status"].value_counts(dropna=False)
)


# ==========================================
# INVESTIGATING DELIVERED ORDER ANOMALIES
# ==========================================

print("\n========== DELIVERED ORDER ANOMALIES ==========")

# Delivered orders missing customer delivery dates
missing_customer_date = orders[
    (orders["order_status"] == "delivered") &
    (orders["order_delivered_customer_date"].isnull())
]

print("\nDelivered orders missing customer delivery dates:")
print(
    missing_customer_date[
        [
            "order_id",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_estimated_delivery_date"
        ]
    ].to_string(index=False)
)

# Delivered orders missing carrier delivery dates
missing_carrier_date = orders[
    (orders["order_status"] == "delivered") &
    (orders["order_delivered_carrier_date"].isnull())
]

print("\nDelivered orders missing carrier delivery dates:")
print(missing_carrier_date["order_id"].to_string(index=False))

# Delivered orders missing approval dates
missing_approval_date = orders[
    (orders["order_status"] == "delivered") &
    (orders["order_approved_at"].isnull())
]

print("\nDelivered orders missing approval dates:")
print(missing_approval_date["order_id"].to_string(index=False))

# ==========================================
# DATE CONVERSION AND VALIDATION
# ==========================================

orders_clean = orders.copy()

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

# Convert columns into datetime format
for column in date_columns:
    orders_clean[column] = pd.to_datetime(
        orders_clean[column],
        errors="coerce"
    )

print("\n========== DATE DATA TYPES ==========")
print(orders_clean[date_columns].dtypes)

# Check missing values after conversion
print("\n========== MISSING DATE VALUES ==========")
print(orders_clean[date_columns].isnull().sum())

# Check chronological inconsistencies
invalid_approval = orders_clean[
    orders_clean["order_approved_at"].notna() &
    (orders_clean["order_approved_at"] <
     orders_clean["order_purchase_timestamp"])
]

invalid_carrier = orders_clean[
    orders_clean["order_delivered_carrier_date"].notna() &
    orders_clean["order_approved_at"].notna() &
    (orders_clean["order_delivered_carrier_date"] <
     orders_clean["order_approved_at"])
]

invalid_delivery = orders_clean[
    orders_clean["order_delivered_customer_date"].notna() &
    orders_clean["order_delivered_carrier_date"].notna() &
    (orders_clean["order_delivered_customer_date"] <
     orders_clean["order_delivered_carrier_date"])
]

print("\n========== CHRONOLOGICAL VALIDATION ==========")
print("Approval before purchase:", len(invalid_approval))
print("Carrier delivery before approval:", len(invalid_carrier))
print("Customer delivery before carrier delivery:", len(invalid_delivery))

# ==========================================
# INVESTIGATE CHRONOLOGICAL INCONSISTENCIES
# ==========================================

# Carrier handover before approval
carrier_before_approval = orders_clean[
    orders_clean["order_delivered_carrier_date"].notna() &
    orders_clean["order_approved_at"].notna() &
    (
        orders_clean["order_delivered_carrier_date"] <
        orders_clean["order_approved_at"]
    )
].copy()

carrier_before_approval["time_difference_hours"] = (
    carrier_before_approval["order_approved_at"] -
    carrier_before_approval["order_delivered_carrier_date"]
).dt.total_seconds() / 3600

print("\n========== CARRIER DATE INCONSISTENCIES ==========")
print("Total:", len(carrier_before_approval))

print("\nOrder status breakdown:")
print(carrier_before_approval["order_status"].value_counts())

print("\nTime difference in hours:")
print(carrier_before_approval["time_difference_hours"].describe())

print("\nSample records:")
print(
    carrier_before_approval[
        [
            "order_id",
            "order_status",
            "order_approved_at",
            "order_delivered_carrier_date",
            "time_difference_hours"
        ]
    ].head(10).to_string(index=False)
)


# Customer delivery before carrier handover
customer_before_carrier = orders_clean[
    orders_clean["order_delivered_customer_date"].notna() &
    orders_clean["order_delivered_carrier_date"].notna() &
    (
        orders_clean["order_delivered_customer_date"] <
        orders_clean["order_delivered_carrier_date"]
    )
].copy()

print("\n========== CUSTOMER DELIVERY INCONSISTENCIES ==========")
print("Total:", len(customer_before_carrier))

print("\nOrder status breakdown:")
print(customer_before_carrier["order_status"].value_counts())

print("\nSample records:")
print(
    customer_before_carrier[
        [
            "order_id",
            "order_status",
            "order_delivered_carrier_date",
            "order_delivered_customer_date"
        ]
    ].head(10).to_string(index=False)
)

# ==========================================
# CREATE DATA QUALITY FLAGS
# ==========================================

# Flag carrier date earlier than approval date
orders_clean["flag_carrier_before_approval"] = (
    orders_clean["order_approved_at"].notna() &
    orders_clean["order_delivered_carrier_date"].notna() &
    (
        orders_clean["order_delivered_carrier_date"] <
        orders_clean["order_approved_at"]
    )
)

# Flag customer delivery earlier than carrier date
orders_clean["flag_customer_before_carrier"] = (
    orders_clean["order_delivered_customer_date"].notna() &
    orders_clean["order_delivered_carrier_date"].notna() &
    (
        orders_clean["order_delivered_customer_date"] <
        orders_clean["order_delivered_carrier_date"]
    )
)

# Valid delivery duration records
valid_delivery = (
    orders_clean["order_delivered_customer_date"].notna() &
    orders_clean["order_delivered_carrier_date"].notna() &
    (
        orders_clean["order_delivered_customer_date"] >=
        orders_clean["order_delivered_carrier_date"]
    )
)

orders_clean["delivery_duration_days"] = np.where(
    valid_delivery,
    (
        orders_clean["order_delivered_customer_date"] -
        orders_clean["order_delivered_carrier_date"]
    ).dt.total_seconds() / 86400,
    np.nan
)

print("\n========== FINAL ORDER QUALITY FLAGS ==========")
print("Carrier before approval:",
      orders_clean["flag_carrier_before_approval"].sum())

print("Customer before carrier:",
      orders_clean["flag_customer_before_carrier"].sum())

print("Valid delivery duration records:",
      valid_delivery.sum())

# Save the analysis-ready orders dataset
orders_clean.to_csv("orders_analysis_ready.csv", index=False)

print("\nAnalysis-ready orders dataset saved successfully!")