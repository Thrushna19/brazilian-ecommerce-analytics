import pandas as pd
import csv

# Load original review dataset
reviews = pd.read_csv(
    "../Dataset/olist_order_reviews_dataset.csv"
)

print("Original rows:", len(reviews))

# Replace line breaks inside review comments with spaces
text_columns = [
    "review_comment_title",
    "review_comment_message"
]

for column in text_columns:
    reviews[column] = (
        reviews[column]
        .fillna("")
        .str.replace(r"[\r\n]+", " ", regex=True)
    )

# Save a MySQL-friendly CSV
reviews.to_csv(
    "../Dataset/olist_order_reviews_mysql.csv",
    index=False,
    encoding="utf-8",
    quoting=csv.QUOTE_ALL,
    escapechar="\\",
    doublequote=False,
    lineterminator="\n"
)

print("Cleaned rows:", len(reviews))
print("File saved successfully!")

