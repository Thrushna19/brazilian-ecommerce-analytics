SELECT
    DATE_FORMAT(review_creation_date, '%Y-%m') AS review_month,
    COUNT(*) AS total_reviews,
    ROUND(AVG(review_score), 2) AS average_rating,
    ROUND(
        SUM(CASE WHEN review_score <= 2 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS negative_review_percentage
FROM order_reviews
GROUP BY DATE_FORMAT(review_creation_date, '%Y-%m')
ORDER BY review_month;

DESCRIBE orders;