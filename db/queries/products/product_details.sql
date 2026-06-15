-- ==========================================================
-- Product Details
-- Returns detailed statistics for a single product
-- ==========================================================

SELECT

    p.product_sk,

    p.product_id,

    p.product_name,

    p.category,

    p.subcategory,

    COUNT(DISTINCT f.order_id)          AS total_orders,

    COUNT(DISTINCT f.customer_sk)       AS unique_customers,

    SUM(f.quantity)                     AS total_quantity_sold,

    ROUND(
        SUM(f.sales_amount),
        2
    )                                   AS total_revenue,

    ROUND(
        SUM(f.profit),
        2
    )                                   AS total_profit,

    ROUND(
        AVG(f.sales_amount),
        2
    )                                   AS average_sale,

    ROUND(
        AVG(f.discount),
        4
    )                                   AS average_discount,

    MIN(d.full_date)                    AS first_sale_date,

    MAX(d.full_date)                    AS last_sale_date

FROM fact_sales AS f

INNER JOIN dim_product AS p

    ON p.product_sk = f.product_sk

INNER JOIN dim_date AS d

    ON d.date_sk = f.order_date_sk

WHERE

    p.product_id = :product_id

GROUP BY

    p.product_sk,
    p.product_id,
    p.product_name,
    p.category,
    p.subcategory;