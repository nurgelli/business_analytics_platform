-- Revenue grouped by region

SELECT

    c.region,

    COUNT(DISTINCT f.order_id) AS total_orders,

    COUNT(DISTINCT c.customer_sk) AS total_customers,

    ROUND(
        SUM(f.sales_amount),
        2
    ) AS total_revenue,

    ROUND(
        SUM(f.profit),
        2
    ) AS total_profit,

    ROUND(
        AVG(f.sales_amount),
        2
    ) AS average_order_value

FROM fact_sales AS f

INNER JOIN dim_customer AS c

    ON c.customer_sk = f.customer_sk

GROUP BY

    c.region

ORDER BY

    total_revenue DESC;