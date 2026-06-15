-- Revenue by Category / Subcategory

SELECT

    p.category,

    p.subcategory,

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

INNER JOIN dim_product AS p

    ON p.product_sk = f.product_sk

GROUP BY

    p.category,
    p.subcategory

ORDER BY

    total_revenue DESC;