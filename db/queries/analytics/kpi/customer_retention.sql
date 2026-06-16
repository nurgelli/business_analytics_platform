WITH base AS (
    SELECT DISTINCT
        customer_sk
    FROM fact_sales AS f
    INNER JOIN dim_date AS d
        ON d.date_sk = f.order_date_sk
    WHERE
        d.year = :base_year
),
next AS (
    SELECT DISTINCT
        customer_sk
    FROM fact_sales AS f
    INNER JOIN dim_date AS d
        ON d.date_sk = f.order_date_sk
    WHERE
        d.year = :next_year)
SELECT
    COUNT(base.customer_sk) AS base_customers,
    COUNT(next.customer_sk) AS retained_customers,
    ROUND(COUNT(next.customer_sk)::numeric / NULLIF(COUNT(base.customer_sk), 0) * 100, 2) AS retention_rate_pct
FROM base
LEFT JOIN next
USING (
    customer_sk
);