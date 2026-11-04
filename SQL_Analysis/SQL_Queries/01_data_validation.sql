USE olist_analytics;

LOAD DATA LOCAL INFILE 'C:/Users/HP/Ecommerce_Analytics/Dataset/olist_order_reviews_mysql.csv'
INTO TABLE order_reviews
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
ESCAPED BY '\\'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

SELECT COUNT(*) AS total_reviews
FROM order_reviews;

SELECT *
FROM order_reviews
LIMIT 5;

