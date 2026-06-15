SELECT

    SUM(f.sales_amount) AS total_revenue,

    SUM(f.profit) AS total_profit,

    COUNT(DISTINCT f.order_id) AS total_orders,

    COUNT(DISTINCT f.customer_sk) AS unique_customers,

    ROUND(

        SUM(f.profit)

        /

        NULLIF(

            SUM(f.sales_amount),

            0

        ) * 100,

        2

    ) AS profit_margin_pct

FROM fact_sales AS f

INNER JOIN dim_date AS d

    ON d.date_sk = f.order_date_sk

WHERE

    (

        :year IS NULL

        OR

        d.year = :year

    );