WITH seller_revenue AS (
    SELECT
        oi.seller_id,
        SUM(oi.price) AS seller_revenue
    FROM olist_order_items_dataset oi
    INNER JOIN orders o
        ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY oi.seller_id
),

seller_shares AS (
    SELECT
        seller_id,
        seller_revenue,
        SUM(seller_revenue) OVER () AS total_revenue,
        seller_revenue * 100.0 /
        SUM(seller_revenue) OVER () AS revenue_share
    FROM seller_revenue
),

ranked_sellers AS (
    SELECT
        seller_id,
        seller_revenue,
        revenue_share,
        DENSE_RANK() OVER (
            ORDER BY seller_revenue DESC
        ) AS seller_rank
    FROM seller_shares
)

SELECT
    COUNT(*) AS total_sellers,
    ROUND(SUM(
        CASE
            WHEN seller_rank <= 10
            THEN revenue_share
            ELSE 0
        END
    ), 2) AS top_10_revenue_share_percentage,
    ROUND(SUM(POWER(revenue_share, 2)), 2) AS marketplace_hhi
FROM ranked_sellers;

