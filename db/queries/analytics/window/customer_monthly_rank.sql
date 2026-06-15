-- 1. Her müşteri için aylık satış sıralaması
SELECT
    c.customer_name,
    c.segment,
    d.year,
    d.month,
    SUM(f.sales_amount) AS monthly_revenue,
    RANK() OVER (
        PARTITION BY d.year, d.month
        ORDER BY SUM(f.sales_amount) DESC
    ) AS revenue_rank,
    LAG(SUM(f.sales_amount)) OVER (
        PARTITION BY c.customer_sk
        ORDER BY d.year, d.month
    ) AS prev_month_revenue,
    SUM(f.sales_amount) - LAG(SUM(f.sales_amount)) OVER (
        PARTITION BY c.customer_sk
        ORDER BY d.year, d.month
    ) AS month_over_month_change
FROM fact_sales f
JOIN dim_customer c ON f.customer_sk = c.customer_sk
JOIN dim_date d ON f.order_date_sk = d.date_sk
GROUP BY c.customer_sk, c.customer_name, c.segment, d.year, d.month;