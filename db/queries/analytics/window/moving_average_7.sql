-- 3. Moving Average (7 günlük)
WITH daily_sales AS (
    SELECT
        d.full_date,
        SUM(f.sales_amount) AS revenue
    FROM fact_sales f
    JOIN dim_date d ON f.order_date_sk = d.date_sk
    GROUP BY d.full_date
)
SELECT
    full_date,
    revenue,
    AVG(revenue) OVER (
        ORDER BY full_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7d
FROM daily_sales;