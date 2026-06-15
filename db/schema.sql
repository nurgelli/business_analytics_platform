-- db/schema.sql

-- Dimension: Customer
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
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_monthly_revenue AS
SELECT
    d.year,
    d.month,
    d.month_name,
    COUNT(DISTINCT f.order_id)      AS order_count,
    COUNT(DISTINCT f.customer_sk)   AS unique_customers,
    SUM(f.sales_amount)             AS total_revenue,
    SUM(f.profit)                   AS total_profit,
    ROUND(SUM(f.profit) / NULLIF(SUM(f.sales_amount), 0) * 100, 2) AS profit_margin_pct
FROM fact_sales f
JOIN dim_date d ON f.order_date_sk = d.date_sk
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_monthly_revenue
ON mv_monthly_revenue(year, month);