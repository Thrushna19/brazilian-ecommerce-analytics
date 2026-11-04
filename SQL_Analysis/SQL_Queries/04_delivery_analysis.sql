SELECT
    order_id,
    order_status,
    order_purchase_timestamp,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date
FROM orders
WHERE order_status = 'delivered'
LIMIT 10;

SELECT
    COUNT(*) AS total_orders,
    SUM(
        CASE
            WHEN order_delivered_customer_date IS NULL
                 OR order_delivered_customer_date = ''
            THEN 1 ELSE 0
        END
    ) AS missing_delivery_dates,
    SUM(
        CASE
            WHEN order_estimated_delivery_date IS NULL
                 OR order_estimated_delivery_date = ''
            THEN 1 ELSE 0
        END
    ) AS missing_estimated_dates
FROM orders;

SELECT
    COUNT(*) AS delivered_orders,

    ROUND(
        AVG(
            DATEDIFF(
                STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s'),
                STR_TO_DATE(order_purchase_timestamp, '%Y-%m-%d %H:%i:%s')
            )
        ), 2
    ) AS average_delivery_days,

    ROUND(
        AVG(
            DATEDIFF(
                STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s'),
                STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s')
            )
        ), 2
    ) AS average_days_vs_estimate

FROM orders

WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL
AND order_delivered_customer_date != ''
AND order_estimated_delivery_date IS NOT NULL
AND order_estimated_delivery_date != '';

