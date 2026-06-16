SELECT
    d.year,
    d.quarter,
    d.month,
    d.month_name,

    COUNT(DISTINCT f.order_id) AS total_orders,

    SUM(f.quantity) AS total_quantity,

    ROUND(
        SUM(f.sales_amount),
        2
    ) AS total_revenue,

    ROUND(
        SUM(f.profit),
        2
    ) AS total_profit,

    ROUND(
        AVG(f.sales_amount),
        2
    ) AS average_order_value

FROM fact_sales AS f

INNER JOIN dim_date AS d

    ON d.date_sk = f.order_date_sk

GROUP BY

    d.year,
    d.quarter,
    d.month,
    d.month_name

ORDER BY

    d.year,
    d.month;