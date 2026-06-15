-- 6. CTE: En karlı top-10 ürün
WITH product_performance AS (
    SELECT
        p.product_name,
        p.category,
        p.sub_category,
        COUNT(f.sale_sk)          AS units_sold,
        SUM(f.sales_amount)       AS total_revenue,
        SUM(f.profit)             AS total_profit,
        ROUND(
            SUM(f.profit) / NULLIF(SUM(f.sales_amount), 0) * 100, 2
        )                         AS profit_margin
    FROM fact_sales f
    JOIN dim_product p ON f.product_sk = p.product_sk
    GROUP BY p.product_name, p.category, p.sub_category
),
ranked AS (
    SELECT *,
           RANK() OVER (ORDER BY total_profit DESC) AS profit_rank
    FROM product_performance
)
SELECT * FROM ranked WHERE profit_rank <= 10;