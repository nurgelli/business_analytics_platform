SELECT
    d.year,
    d.quarter,
    d.month,
    d.month_name,
    COUNT(DISTINCT f.order_id)  AS total_orders,
    COUNT(DISTINCT f.customer_sk) AS total_customers,
    SUM(f.quantity) AS total_quantity,
    ROUND(SUM(f.sales_amount)::numeric, 2)    AS total_sales,
    ROUND(SUM(f.profit)::numeric, 2) AS total_profit,
    ROUND(AVG(f.sales_amount)::numeric,2) AS avg_order_value,
    ROUND(CASE WHEN SUM(f.sales_amount) = 0
            THEN 0
            ELSE
                SUM(f.profit)
                / SUM(f.sales_amount)
                * 100
        END
    ,2) AS profit_margin_pct

FROM fact_sales f
INNER JOIN dim_date d
ON f.order_date_sk = d.date_sk
GROUP BY
    d.year,
    d.quarter,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;