FROM customer_orders;

WITH payment_analysis AS (
    SELECT
        p.payment_type,
        COUNT(DISTINCT p.order_id) AS total_orders,
        SUM(p.payment_value) AS total_payment_value,
        AVG(p.payment_installments) AS average_installments
    FROM olist_order_payments_dataset p
    INNER JOIN orders o
        ON p.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY p.payment_type
)

SELECT
    payment_type,
    total_orders,
    ROUND(total_payment_value, 2) AS total_payment_value,
    ROUND(
        total_payment_value * 100.0 /
        SUM(total_payment_value) OVER (),
        2
    ) AS payment_value_percentage,
    ROUND(average_installments, 2) AS average_installments
FROM payment_analysis
ORDER BY total_payment_value DESC;