import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
orders = pd.read_csv("../Dataset/olist_orders_dataset.csv")
order_items = pd.read_csv("../Dataset/olist_order_items_dataset.csv")

# Convert purchase timestamp
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

print("Datasets loaded successfully!")

# Select completed orders
completed_orders = orders[
    orders["order_status"] == "delivered"
].copy()

# Merge orders with order items
sales = order_items.merge(
    completed_orders[
        ["order_id", "order_purchase_timestamp"]
    ],
    on="order_id",
    how="inner"
)

print("\n========== SALES DATA ==========")

print("Total order items:", len(sales))
print("Unique orders:", sales["order_id"].nunique())

# Calculate product revenue and freight
product_revenue = sales["price"].sum()
freight_revenue = sales["freight_value"].sum()
total_value = product_revenue + freight_revenue

print("\nProduct Revenue:", round(product_revenue, 2))
print("Freight Value:", round(freight_revenue, 2))
print("Total Order Item Value:", round(total_value, 2))


# ==========================================
# BUSINESS PERFORMANCE KPIs
# ==========================================

total_orders = sales["order_id"].nunique()
total_items = len(sales)

average_order_value = product_revenue / total_orders

average_items_per_order = total_items / total_orders

average_product_price = sales["price"].mean()

print("\n========== BUSINESS KPIs ==========")

print("Completed Orders:", total_orders)
print("Items Sold:", total_items)

print("Average Order Value:",
      round(average_order_value, 2))

print("Average Items per Order:",
      round(average_items_per_order, 2))

print("Average Product Price:",
      round(average_product_price, 2))

# ==========================================
# MONTHLY REVENUE ANALYSIS
# ==========================================

# Extract purchase month
sales["order_month"] = (
    sales["order_purchase_timestamp"].dt.to_period("M")
)

# Aggregate monthly performance
monthly_sales = (
    sales.groupby("order_month")
    .agg(
        product_revenue=("price", "sum"),
        freight_value=("freight_value", "sum"),
        total_orders=("order_id", "nunique"),
        items_sold=("order_id", "count")
    )
    .reset_index()
)

# Calculate average order value
monthly_sales["average_order_value"] = (
    monthly_sales["product_revenue"] /
    monthly_sales["total_orders"]
)

# Convert month into string for visualisation
monthly_sales["order_month"] = (
    monthly_sales["order_month"].astype(str)
)

print("\n========== MONTHLY SALES PERFORMANCE ==========")
print(monthly_sales.to_string(index=False))

# Identify best-performing month
best_month = monthly_sales.loc[
    monthly_sales["product_revenue"].idxmax()
]

print("\n========== BEST PERFORMING MONTH ==========")
print("Month:", best_month["order_month"])
print("Revenue:", round(best_month["product_revenue"], 2))
print("Orders:", best_month["total_orders"])

# ==========================================
# MONTHLY REVENUE VISUALISATION
# ==========================================

plt.figure(figsize=(14, 6))

sns.lineplot(
    data=monthly_sales,
    x="order_month",
    y="product_revenue",
    marker="o"
)

plt.title("Monthly Product Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Product Revenue (BRL)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("../Visualizations/monthly_revenue_trend.png")
plt.show()

# ==========================================
# PRODUCT CATEGORY ANALYSIS
# ==========================================

products = pd.read_csv(
    "../Dataset/olist_products_dataset.csv"
)

category_translation = pd.read_csv(
    "../Dataset/product_category_name_translation.csv"
)

print("Product datasets loaded successfully!")

# Merge sales with product information
product_sales = sales.merge(
    products[
        ["product_id", "product_category_name"]
    ],
    on="product_id",
    how="left"
)

# Translate Portuguese category names into English
product_sales = product_sales.merge(
    category_translation,
    on="product_category_name",
    how="left"
)

# Handle missing category names
product_sales["product_category_name_english"] = (
    product_sales["product_category_name_english"]
    .fillna("Uncategorized")
)

print("\nProduct category data prepared!")

# ==========================================
# CATEGORY PERFORMANCE
# ==========================================

category_sales = (
    product_sales.groupby("product_category_name_english")
    .agg(
        product_revenue=("price", "sum"),
        items_sold=("order_item_id", "count"),
        total_orders=("order_id", "nunique"),
        average_item_price=("price", "mean"),
        unique_products=("product_id", "nunique")
    )
    .reset_index()
)

# Sort categories by revenue
category_sales = category_sales.sort_values(
    by="product_revenue",
    ascending=False
)

print("\n========== TOP 10 CATEGORIES BY REVENUE ==========")

print(
    category_sales.head(10).to_string(index=False)
)

print("\n========== TOP 10 CATEGORIES BY DEMAND ==========")

top_demand = category_sales.sort_values(
    by="items_sold",
    ascending=False
)

print(
    top_demand.head(10).to_string(index=False)
)

# ==========================================
# CATEGORY REVENUE VISUALISATION
# ==========================================

top_10_revenue = category_sales.head(10)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_10_revenue,
    x="product_revenue",
    y="product_category_name_english"
)

plt.title("Top 10 Product Categories by Revenue")
plt.xlabel("Product Revenue (BRL)")
plt.ylabel("Product Category")
plt.tight_layout()

plt.savefig(
    "../Visualizations/top_10_categories_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# CUSTOMER BEHAVIOUR ANALYSIS
# ==========================================

customers = pd.read_csv(
    "../Dataset/olist_customers_dataset.csv"
)

# Merge completed orders with customer information
customer_sales = completed_orders.merge(
    customers[
        ["customer_id", "customer_unique_id", "customer_state"]
    ],
    on="customer_id",
    how="left"
)

print("Customer data prepared successfully!")

# ==========================================
# CUSTOMER KPIs
# ==========================================

customer_order_counts = (
    customer_sales.groupby("customer_unique_id")
    .agg(
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

total_customers = customer_order_counts[
    "customer_unique_id"
].nunique()

repeat_customers = (
    customer_order_counts["total_orders"] > 1
).sum()

repeat_customer_rate = (
    repeat_customers / total_customers
) * 100

average_orders_per_customer = (
    customer_order_counts["total_orders"].mean()
)

print("\n========== CUSTOMER KPIs ==========")

print("Unique Customers:", total_customers)

print("Repeat Customers:", repeat_customers)

print("Repeat Customer Rate:",
      round(repeat_customer_rate, 2), "%")

print("Average Orders per Customer:",
      round(average_orders_per_customer, 2))

# ==========================================
# CUSTOMER GEOGRAPHICAL DISTRIBUTION
# ==========================================

state_customers = (
    customer_sales.groupby("customer_state")
    ["customer_unique_id"]
    .nunique()
    .sort_values(ascending=False)
)

print("\n========== TOP 10 STATES BY CUSTOMERS ==========")

print(state_customers.head(10))

# ==========================================
# SELLER PERFORMANCE ANALYSIS
# ==========================================

sellers = pd.read_csv(
    "../Dataset/olist_sellers_dataset.csv"
)

# Merge sales with seller information
seller_sales = sales.merge(
    sellers[
        ["seller_id", "seller_state"]
    ],
    on="seller_id",
    how="left"
)

print("Seller data prepared successfully!")

# ==========================================
# SELLER KPIs
# ==========================================

seller_performance = (
    seller_sales.groupby("seller_id")
    .agg(
        product_revenue=("price", "sum"),
        items_sold=("order_item_id", "count"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

seller_performance = seller_performance.sort_values(
    by="product_revenue",
    ascending=False
)

print("\n========== TOP 10 SELLERS BY REVENUE ==========")

print(
    seller_performance.head(10).to_string(index=False)
)

print("\nTotal Active Sellers:",
      seller_performance["seller_id"].nunique())

# ==========================================
# SELLER REVENUE CONCENTRATION
# ==========================================

total_seller_revenue = seller_performance[
    "product_revenue"
].sum()

seller_performance["revenue_share"] = (
    seller_performance["product_revenue"] /
    total_seller_revenue
) * 100

seller_performance["cumulative_revenue_share"] = (
    seller_performance["revenue_share"].cumsum()
)

top_10_seller_share = (
    seller_performance.head(10)["product_revenue"].sum()
    / total_seller_revenue
) * 100

print("\n========== SELLER CONCENTRATION ==========")

print("Top 10 sellers revenue share:",
      round(top_10_seller_share, 2), "%")

print("Top 10 sellers:")
print(
    seller_performance.head(10).to_string(index=False)
)

# ==========================================
# PRICE AND FREIGHT ANALYSIS
# ==========================================

price_freight_analysis = (
    product_sales.groupby("product_category_name_english")
    .agg(
        average_product_price=("price", "mean"),
        average_freight=("freight_value", "mean"),
        items_sold=("order_item_id", "count"),
        product_revenue=("price", "sum")
    )
    .reset_index()
)

# Calculate freight as a percentage of product price
price_freight_analysis["freight_to_price_ratio"] = (
    price_freight_analysis["average_freight"] /
    price_freight_analysis["average_product_price"]
) * 100

print("\n========== TOP 10 CATEGORIES BY AVERAGE PRICE ==========")

print(
    price_freight_analysis.sort_values(
        by="average_product_price",
        ascending=False
    ).head(10).to_string(index=False)
)

print("\n========== TOP 10 CATEGORIES BY AVERAGE FREIGHT ==========")

print(
    price_freight_analysis.sort_values(
        by="average_freight",
        ascending=False
    ).head(10).to_string(index=False)
)

# ==========================================
# PRICE VS FREIGHT VISUALISATION
# ==========================================

plt.figure(figsize=(10, 7))

sns.scatterplot(
    data=price_freight_analysis,
    x="average_product_price",
    y="average_freight",
    size="items_sold",
    sizes=(40, 400),
    alpha=0.7
)

plt.title("Relationship Between Product Price and Freight")
plt.xlabel("Average Product Price (BRL)")
plt.ylabel("Average Freight Value (BRL)")
plt.tight_layout()

plt.savefig(
    "../Visualizations/price_vs_freight.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# SAVE DAY 3 ANALYSIS OUTPUTS
# ==========================================

category_sales.to_csv(
    "../Visualizations/category_performance.csv",
    index=False
)

customer_order_counts.to_csv(
    "../Visualizations/customer_order_analysis.csv",
    index=False
)

seller_performance.to_csv(
    "../Visualizations/seller_performance.csv",
    index=False
)

price_freight_analysis.to_csv(
    "../Visualizations/price_freight_analysis.csv",
    index=False
)

monthly_sales.to_csv(
    "../Visualizations/monthly_sales_performance.csv",
    index=False
)

print("\nAll Day 3 analysis files saved successfully!")

# ==========================================
# MICROECONOMICS: PRICE AND DEMAND ANALYSIS
# ==========================================

# Category-level price and demand
demand_price = (
    product_sales.groupby("product_category_name_english")
    .agg(
        average_price=("price", "mean"),
        quantity_demanded=("order_item_id", "count"),
        product_revenue=("price", "sum"),
        unique_products=("product_id", "nunique")
    )
    .reset_index()
)

# Exclude categories with no valid prices or quantities
demand_price = demand_price[
    (demand_price["average_price"] > 0) &
    (demand_price["quantity_demanded"] > 0)
].copy()

print("\n========== PRICE AND DEMAND ANALYSIS ==========")

print(
    demand_price.sort_values(
        "quantity_demanded",
        ascending=False
    ).head(10).to_string(index=False)
)

# Pearson correlation
pearson_corr = demand_price[
    ["average_price", "quantity_demanded"]
].corr(method="pearson").iloc[0, 1]

# Spearman correlation
spearman_corr = demand_price[
    ["average_price", "quantity_demanded"]
].corr(method="spearman").iloc[0, 1]

print("\n========== PRICE-DEMAND CORRELATION ==========")

print("Pearson correlation:", round(pearson_corr, 3))
print("Spearman correlation:", round(spearman_corr, 3))

# ==========================================
# PRICE AND DEMAND SCATTER PLOT
# ==========================================

plt.figure(figsize=(11, 7))

sns.regplot(
    data=demand_price,
    x="average_price",
    y="quantity_demanded",
    scatter_kws={"alpha": 0.65},
    line_kws={"color": "red"}
)

plt.title("Relationship Between Average Product Price and Demand")
plt.xlabel("Average Product Price (BRL)")
plt.ylabel("Items Sold")
plt.tight_layout()

plt.savefig(
    "../Visualizations/price_demand_relationship.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# MARKET CONCENTRATION: HHI
# ==========================================

seller_market_share = seller_performance.copy()

# Calculate percentage market share
seller_market_share["market_share"] = (
    seller_market_share["product_revenue"] /
    seller_market_share["product_revenue"].sum()
) * 100

# Square individual market shares
seller_market_share["market_share_squared"] = (
    seller_market_share["market_share"] ** 2
)

# Calculate HHI
hhi = seller_market_share["market_share_squared"].sum()

print("\n========== MARKET CONCENTRATION ANALYSIS ==========")

print("Total sellers:", len(seller_market_share))
print("HHI:", round(hhi, 2))

print("\nTop 10 sellers by market share:")

print(
    seller_market_share[
        ["seller_id", "market_share"]
    ].head(10).to_string(index=False)
)

# ==========================================
# MICROECONOMICS: CONSUMER TRADE-OFFS
# ==========================================

order_cost_analysis = (
    sales.groupby("order_id")
    .agg(
        product_value=("price", "sum"),
        freight_value=("freight_value", "sum"),
        items_purchased=("order_item_id", "count")
    )
    .reset_index()
)

# Calculate total purchase cost
order_cost_analysis["total_purchase_cost"] = (
    order_cost_analysis["product_value"] +
    order_cost_analysis["freight_value"]
)

# Calculate freight as percentage of product value
order_cost_analysis["freight_percentage"] = (
    order_cost_analysis["freight_value"] /
    order_cost_analysis["product_value"]
) * 100

print("\n========== CONSUMER PURCHASING COST ==========")

print(
    order_cost_analysis[
        [
            "product_value",
            "freight_value",
            "total_purchase_cost",
            "freight_percentage"
        ]
    ].describe().round(2)
)

# Orders where freight exceeds 20% of product value
high_freight_orders = order_cost_analysis[
    order_cost_analysis["freight_percentage"] > 20
]

high_freight_percentage = (
    len(high_freight_orders) /
    len(order_cost_analysis)
) * 100

print("\n========== FREIGHT BURDEN ANALYSIS ==========")

print("Orders with freight above 20%:",
      len(high_freight_orders))

print("Percentage of orders:",
      round(high_freight_percentage, 2), "%")

print("Average freight percentage:",
      round(order_cost_analysis["freight_percentage"].mean(), 2), "%")

plt.figure(figsize=(10, 6))

sns.histplot(
    data=order_cost_analysis,
    x="freight_percentage",
    bins=40,
    kde=True
)

plt.title("Distribution of Freight as a Percentage of Product Value")
plt.xlabel("Freight Percentage (%)")
plt.ylabel("Number of Orders")
plt.tight_layout()

plt.savefig(
    "../Visualizations/consumer_freight_burden.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# CONSUMER PURCHASING COST ANALYSIS
# ==========================================

order_cost_analysis = (
    sales.groupby("order_id")
    .agg(
        product_value=("price", "sum"),
        freight_value=("freight_value", "sum"),
        items_purchased=("order_item_id", "count")
    )
    .reset_index()
)

# Calculate total purchase cost
order_cost_analysis["total_purchase_cost"] = (
    order_cost_analysis["product_value"] +
    order_cost_analysis["freight_value"]
)

# Calculate freight as a percentage of product value
order_cost_analysis["freight_percentage"] = (
    order_cost_analysis["freight_value"] /
    order_cost_analysis["product_value"]
) * 100

# Summary table
consumer_freight_summary = (
    order_cost_analysis[
        [
            "product_value",
            "freight_value",
            "total_purchase_cost",
            "freight_percentage"
        ]
    ]
    .describe()
    .round(2)
)

print("\n========== CONSUMER FREIGHT BURDEN SUMMARY ==========")
print(consumer_freight_summary)

# Orders where freight exceeds 20% of product value
high_freight_orders = order_cost_analysis[
    order_cost_analysis["freight_percentage"] > 20
]

high_freight_percentage = (
    len(high_freight_orders) /
    len(order_cost_analysis)
) * 100

print("\n========== FREIGHT BURDEN ANALYSIS ==========")
print("Total orders:", len(order_cost_analysis))
print("Orders with freight above 20%:", len(high_freight_orders))
print("Percentage of orders:", round(high_freight_percentage, 2), "%")

# Save detailed order-level table
order_cost_analysis.to_csv(
    "../Visualizations/consumer_freight_analysis.csv",
    index=False
)

# Save summary table
consumer_freight_summary.to_csv(
    "../Visualizations/consumer_freight_summary.csv"
)

print("\nConsumer freight analysis saved successfully!")