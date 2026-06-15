-- Product Sales Summary

SELECT

    p.product_sk,

    p.product_id,

    p.product_name,

    p.category,

    p.subcategory,

    SUM(f.quantity) AS total_units_sold,

    ROUND(
        SUM(f.sales_amount),
        2
    ) AS total_revenue,

    ROUND(
        SUM(f.profit),
        2
    ) AS total_profit,

    COUNT(DISTINCT f.order_id) AS order_count

FROM fact_sales AS f

INNER JOIN dim_product AS p

    ON p.product_sk = f.product_sk

GROUP BY

    p.product_sk,
    p.product_id,
    p.product_name,
    p.category,
    p.subcategory

ORDER BY

    total_units_sold DESC,
    total_revenue DESC;