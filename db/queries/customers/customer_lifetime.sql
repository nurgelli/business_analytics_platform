-- Customer Lifetime Value (CLV / LTV)

SELECT
    c.customer_sk,
    c.customer_id,
    c.customer_name,
    c.segment,
    c.region,

    COUNT(DISTINCT f.order_id) AS total_orders,

    SUM(f.quantity) AS total_quantity,

    ROUND(
        SUM(f.sales_amount),
        2
    ) AS lifetime_revenue,

    ROUND(
        SUM(f.profit),
        2
    ) AS lifetime_profit,

    ROUND(
        AVG(f.sales_amount),
        2
    ) AS average_order_value,

    ROUND(
        SUM(f.sales_amount)
        /
        NULLIF(
            COUNT(DISTINCT f.order_id),
            0
        ),
        2
    ) AS revenue_per_order

FROM fact_sales AS f

INNER JOIN dim_customer AS c
    ON c.customer_sk = f.customer_sk

GROUP BY

    c.customer_sk,
    c.customer_id,
    c.customer_name,
    c.segment,
    c.region

ORDER BY

    lifetime_revenue DESC;