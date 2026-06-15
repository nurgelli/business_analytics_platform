DROP MATERIALIZED VIEW IF EXISTS mv_customer_summary CASCADE;

CREATE MATERIALIZED VIEW mv_customer_summary AS
SELECT
    c.customer_sk,
    c.customer_name,
    c.segment,
    COUNT(DISTINCT f.order_id) AS order_count,
    SUM(f.sales_amount) AS lifetime_sales,
    SUM(f.profit) AS lifetime_profit,
    MAX(d.date) AS last_purchase_date,
    MIN(d.date) AS first_purchase_date
FROM fact_sales f
JOIN dim_customer c
ON f.customer_sk = c.customer_sk
JOIN dim_date d
ON f.order_date_sk = d.date_sk
GROUP BY
    c.customer_sk,
    c.customer_name,
    c.segment;
CREATE UNIQUE INDEX idx_mv_customer_summary
ON mv_customer_summary(customer_sk);