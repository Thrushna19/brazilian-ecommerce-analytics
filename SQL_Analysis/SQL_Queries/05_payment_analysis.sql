WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(
            STR_TO_DATE(o.order_purchase_timestamp, '%Y-%m-%d %H:%i:%s'),
            '%Y-%m'
        ) AS sales_month,
        ROUND(SUM(oi.price), 2) AS monthly_revenue
    FROM orders o
    INNER JOIN olist_order_items_dataset oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY sales_month
),

revenue_growth AS (
    SELECT
        sales_month,
        monthly_revenue,
        LAG(monthly_revenue) OVER (
            ORDER BY sales_month
        ) AS previous_month_revenue
    FROM monthly_sales
)

SELECT
    sales_month,
    monthly_revenue,
    previous_month_revenue,
    ROUND(
        (monthly_revenue - previous_month_revenue)
        / NULLIF(previous_month_revenue, 0) * 100,
        2
    ) AS growth_percentage
FROM revenue_growth
ORDER BY sales_month;

WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS total_orders
    FROM customers c
    INNER JOIN orders o
        ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)

SELECT
    COUNT(*) AS total_customers,

    SUM(
        CASE
            WHEN total_orders > 1 THEN 1
            ELSE 0
        END
    ) AS repeat_customers,

    ROUND(
        SUM(
            CASE
                WHEN total_orders > 1 THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS repeat_customer_percentage,

    ROUND(AVG(total_orders), 2) AS average_orders_per_customer

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