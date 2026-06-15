-- Top customers by lifetime revenue

SELECT
    c.customer_sk,
    c.customer_id,
    c.customer_name,
    c.segment,
    c.region,

    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.sales_amount) AS total_revenue,
    SUM(f.profit) AS total_profit,
    ROUND(
        SUM(f.profit)
        / NULLIF(SUM(f.sales_amount), 0)
        * 100,
        2
    ) AS profit_margin_pct

FROM fact_sales AS f
INNER JOIN dim_customer AS c
    ON f.customer_sk = c.customer_sk
GROUP BY
    c.customer_sk,
    c.customer_id,
    c.customer_name,
    c.segment,
    c.region
ORDER BY
    total_revenue DESC,
    total_profit DESC

LIMIT 25;