CREATE TABLE IF NOT EXISTS dim_customer (
    customer_sk     SERIAL PRIMARY KEY,
    customer_id     VARCHAR(20) UNIQUE NOT NULL,
    customer_name   VARCHAR(100),
    segment         VARCHAR(50),     -- Consumer, Corporate, Home Office
    city            VARCHAR(100),
    state           VARCHAR(100),
    country         VARCHAR(100),
    region          VARCHAR(50),
    postal_code     VARCHAR(20),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Dimension: Product
CREATE TABLE IF NOT EXISTS dim_product (
    product_sk      SERIAL PRIMARY KEY,
    product_id      VARCHAR(20) UNIQUE NOT NULL,
    product_name    VARCHAR(200),
    category        VARCHAR(50),     -- Furniture, Office Supplies, Technology
    sub_category    VARCHAR(50),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Dimension: Date
CREATE TABLE IF NOT EXISTS dim_date (
    date_sk         INTEGER PRIMARY KEY,  -- format: YYYYMMDD
    full_date       DATE NOT NULL,
    year            INTEGER,
    quarter         INTEGER,
    month           INTEGER,
    month_name      VARCHAR(20),
    week            INTEGER,
    day_of_week     INTEGER,
    day_name        VARCHAR(20),
    is_weekend      BOOLEAN
);

-- Fact: Sales
CREATE TABLE IF NOT EXISTS fact_sales (
    sale_sk         SERIAL PRIMARY KEY,
    order_id        VARCHAR(20) NOT NULL,
    order_date_sk   INTEGER REFERENCES dim_date(date_sk),
    ship_date_sk    INTEGER REFERENCES dim_date(date_sk),
    customer_sk     INTEGER REFERENCES dim_customer(customer_sk),
    product_sk      INTEGER REFERENCES dim_product(product_sk),
    ship_mode       VARCHAR(50),
    quantity        INTEGER,
    unit_price      NUMERIC(10, 2),
    discount        NUMERIC(5, 2),
    sales_amount    NUMERIC(12, 2),
    profit          NUMERIC(12, 2),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_fact_sales_date ON fact_sales(order_date_sk);
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer ON fact_sales(customer_sk);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product ON fact_sales(product_sk);


-- Materialized View: Monthly Revenue Summary
DROP MATERIALIZED VIEW IF EXISTS mv_monthly_revenue CASCADE;
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_monthly_revenue AS
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
    ROUND(CASE WHEN SUM(f.sales_amount) = 0 THEN 0 ELSE SUM(f.profit) / SUM(f.sales_amount) * 100 END,2) AS profit_margin_pct
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
CREATE UNIQUE INDEX idx_mv_monthly_revenue ON mv_monthly_revenue (year,month);


--Customer summary materialized view
DROP MATERIALIZED VIEW IF EXISTS mv_customer_summary CASCADE;
CREATE MATERIALIZED VIEW mv_customer_summary AS
SELECT
    c.customer_sk,
    c.customer_name,
    c.segment,
    COUNT(DISTINCT f.order_id) AS order_count,
    SUM(f.sales_amount) AS lifetime_sales,
    SUM(f.profit) AS lifetime_profit,
    MAX(d.full_date) AS last_purchase_date,
    MIN(d.full_date) AS first_purchase_date
FROM fact_sales f
JOIN dim_customer c
ON f.customer_sk = c.customer_sk
JOIN dim_date d
ON f.order_date_sk = d.date_sk
GROUP BY
    c.customer_sk,
    c.customer_name,
    c.segment;
CREATE UNIQUE INDEX idx_mv_customer_summary ON mv_customer_summary(customer_sk);