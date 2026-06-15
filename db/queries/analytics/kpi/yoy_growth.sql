WITH yearly AS (

    SELECT

        d.year,

        SUM(f.sales_amount) AS revenue

    FROM fact_sales AS f

    INNER JOIN dim_date AS d

        ON d.date_sk = f.order_date_sk

    GROUP BY

        d.year

)

SELECT

    year,

    revenue,

    LAG(

        revenue

    ) OVER (

        ORDER BY year

    ) AS prev_revenue,

    ROUND(

        (

            revenue

            -

            LAG(revenue)

            OVER (

                ORDER BY year

            )

        )

        /

        NULLIF(

            LAG(revenue)

            OVER (

                ORDER BY year

            ),

            0

        )

        * 100,

        2

    ) AS yoy_growth_pct

FROM yearly

ORDER BY

    year;