-- Daily Sales Performance

SELECT

    d.full_date,

    COUNT(DISTINCT f.order_id) AS total_orders,

    SUM(f.quantity) AS total_quantity,

    ROUND(
        SUM(f.sales_amount),
        2
    ) AS total_revenue,

    ROUND(
        SUM(f.profit),
        2
    ) AS total_profit

FROM fact_sales AS f

INNER JOIN dim_date AS d

    ON d.date_sk = f.order_date_sk

GROUP BY

    d.full_date

ORDER BY

    d.full_date;