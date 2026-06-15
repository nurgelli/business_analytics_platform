SELECT
    c.customer_id,
    c.customer_name,
    f.order_id,
    d.full_date AS order_date,
    p.product_name,
    p.category,
    p.subcategory,
    f.quantity,
    f.sales_amount,
    f.discount,
    f.profit

FROM fact_sales AS f

INNER JOIN dim_customer AS c

    ON c.customer_sk = f.customer_sk

INNER JOIN dim_product AS p

    ON p.product_sk = f.product_sk

INNER JOIN dim_date AS d

    ON d.date_sk = f.order_date_sk

WHERE

    c.customer_id = :customer_id

ORDER BY

    d.full_date DESC,
    f.order_id;