-- 2. Ürün kategorisine göre kümülatif satış (Running Total)
SELECT
    d.full_date,
    p.category,
    SUM(f.sales_amount) AS daily_revenue,
    SUM(SUM(f.sales_amount)) OVER (
        PARTITION BY p.category
        ORDER BY d.full_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_revenue
FROM fact_sales f
JOIN dim_date d ON f.order_date_sk = d.date_sk
JOIN dim_product p ON f.product_sk = p.product_sk
GROUP BY d.full_date, p.category;
