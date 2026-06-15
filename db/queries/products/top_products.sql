-- Top Products by Revenue

SELECT
    p.product_sk,
    p.product_id,
    p.product_name,
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
    ) AS total_profit,

    ROUND(
        AVG(f.sales_amount),
        2
    ) AS average_sale

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

    total_revenue DESC,
    total_profit DESC;