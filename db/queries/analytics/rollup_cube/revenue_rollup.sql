-- 4. ROLLUP: Hiyerarşik toplamlar (Yıl → Çeyrek → Ay)
SELECT
    COALESCE(CAST(d.year AS VARCHAR), 'ALL YEARS') AS year,
    COALESCE(CAST(d.quarter AS VARCHAR), 'ALL QUARTERS') AS quarter,
    COALESCE(CAST(d.month AS VARCHAR), 'ALL MONTHS') AS month,
    SUM(f.sales_amount) AS total_revenue,
    SUM(f.profit)       AS total_profit
FROM fact_sales f
JOIN dim_date d ON f.order_date_sk = d.date_sk
GROUP BY ROLLUP(d.year, d.quarter, d.month)
ORDER BY d.year, d.quarter, d.month;