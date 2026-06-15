-- 5. CUBE: Segment × Kategori × Bölge çapraz analiz
SELECT
    COALESCE(c.segment, 'ALL')    AS segment,
    COALESCE(p.category, 'ALL')   AS category,
    COALESCE(c.region, 'ALL')     AS region,
    COUNT(DISTINCT f.order_id)    AS orders,
    SUM(f.sales_amount)           AS revenue,
    SUM(f.profit)                 AS profit
FROM fact_sales f
JOIN dim_customer c ON f.customer_sk = c.customer_sk
JOIN dim_product  p ON f.product_sk  = p.product_sk
GROUP BY CUBE(c.segment, p.category, c.region);