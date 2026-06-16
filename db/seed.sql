INSERT INTO dim_date (date_sk, full_date, year, quarter, month, month_name, week, day_of_week, day_name, is_weekend)
VALUES
    (20220101, '2022-01-01', 2022, 1, 1,  'January',  52, 6, 'Saturday',  TRUE),
    (20220215, '2022-02-15', 2022, 1, 2,  'February',  7, 2, 'Tuesday',   FALSE),
    (20220310, '2022-03-10', 2022, 1, 3,  'March',    10, 4, 'Thursday',  FALSE),
    (20220605, '2022-06-05', 2022, 2, 6,  'June',     22, 7, 'Sunday',    TRUE),
    (20220920, '2022-09-20', 2022, 3, 9,  'September',38, 2, 'Tuesday',   FALSE),
    (20221115, '2022-11-15', 2022, 4, 11, 'November', 46, 2, 'Tuesday',   FALSE),
    (20221210, '2022-12-10', 2022, 4, 12, 'December', 49, 6, 'Saturday',  TRUE),
    (20230120, '2023-01-20', 2023, 1, 1,  'January',   3, 5, 'Friday',    FALSE),
    (20230315, '2023-03-15', 2023, 1, 3,  'March',    11, 3, 'Wednesday', FALSE),
    (20230710, '2023-07-10', 2023, 3, 7,  'July',     28, 1, 'Monday',    FALSE),
    (20231105, '2023-11-05', 2023, 4, 11, 'November', 44, 7, 'Sunday',    TRUE),
    (20231220, '2023-12-20', 2023, 4, 12, 'December', 51, 3, 'Wednesday', FALSE)
ON CONFLICT (date_sk) DO NOTHING;

-- ── dim_customer ───────────────────────────────────────────────────────────
INSERT INTO dim_customer (customer_id, customer_name, segment, city, state, country, region, postal_code)
VALUES
    ('CUST-001', 'Alice Martin',   'Consumer',    'New York',    'New York',   'United States', 'East',  '10001'),
    ('CUST-002', 'Bob Thompson',   'Corporate',   'Los Angeles', 'California', 'United States', 'West',  '90001'),
    ('CUST-003', 'Carol White',    'Home Office', 'Chicago',     'Illinois',   'United States', 'Central','60601'),
    ('CUST-004', 'David Lee',      'Consumer',    'Houston',     'Texas',      'United States', 'South', '77001'),
    ('CUST-005', 'Emma Johnson',   'Corporate',   'Phoenix',     'Arizona',    'United States', 'West',  '85001'),
    ('CUST-006', 'Frank Garcia',   'Consumer',    'Philadelphia','Pennsylvania','United States', 'East',  '19101')
ON CONFLICT (customer_id) DO NOTHING;

-- ── dim_product ────────────────────────────────────────────────────────────
INSERT INTO dim_product (product_id, product_name, category, sub_category)
VALUES
    ('PROD-001', 'Staple Remover Pro',         'Office Supplies', 'Fasteners'),
    ('PROD-002', 'Ergonomic Office Chair',     'Furniture',       'Chairs'),
    ('PROD-003', 'Canon Laser Printer MF3110', 'Technology',      'Machines'),
    ('PROD-004', 'A4 Copy Paper 500 Sheet',    'Office Supplies', 'Paper'),
    ('PROD-005', 'Adjustable Standing Desk',   'Furniture',       'Tables'),
    ('PROD-006', 'Logitech MX Master 3 Mouse', 'Technology',      'Accessories')
ON CONFLICT (product_id) DO NOTHING;

-- ── fact_sales ─────────────────────────────────────────────────────────────
INSERT INTO fact_sales
    (order_id, order_date_sk, ship_date_sk, customer_sk, product_sk,
     ship_mode, quantity, unit_price, discount, sales_amount, profit)
SELECT
    v.order_id, v.order_date_sk, v.ship_date_sk,
    c.customer_sk, p.product_sk,
    v.ship_mode, v.quantity, v.unit_price, v.discount,
    ROUND((v.quantity * v.unit_price * (1 - v.discount))::numeric, 2),
    ROUND((v.quantity * v.unit_price * (1 - v.discount) * v.margin)::numeric, 2)
FROM (VALUES
    ('CA-2022-001', 20220101, 20220215, 'CUST-001', 'PROD-001', 'Standard Class', 5,  3.99,  0.00, 0.20),
    ('CA-2022-002', 20220215, 20220310, 'CUST-002', 'PROD-002', 'Second Class',   1,  499.99,0.10, 0.18),
    ('CA-2022-003', 20220310, 20220605, 'CUST-003', 'PROD-003', 'First Class',    2,  379.00,0.20, 0.12),
    ('CA-2022-004', 20220605, 20220920, 'CUST-001', 'PROD-004', 'Standard Class', 10, 6.99,  0.00, 0.30),
    ('CA-2022-005', 20220920, 20221115, 'CUST-004', 'PROD-005', 'Second Class',   1,  799.00,0.15, 0.22),
    ('CA-2022-006', 20221115, 20221210, 'CUST-005', 'PROD-006', 'First Class',    3,  89.99, 0.05, 0.25),
    ('CA-2022-007', 20221210, 20230120, 'CUST-006', 'PROD-001', 'Same Day',       8,  3.99,  0.00, 0.20),
    ('CA-2023-001', 20230120, 20230315, 'CUST-001', 'PROD-003', 'Second Class',   1,  379.00,0.00, 0.14),
    ('CA-2023-002', 20230315, 20230710, 'CUST-002', 'PROD-005', 'First Class',    2,  799.00,0.10, 0.20),
    ('CA-2023-003', 20230710, 20231105, 'CUST-003', 'PROD-006', 'Standard Class', 4,  89.99, 0.00, 0.25),
    ('CA-2023-004', 20231105, 20231220, 'CUST-004', 'PROD-002', 'Second Class',   1,  499.99,0.05, 0.19),
    ('CA-2023-005', 20231220, 20231220, 'CUST-005', 'PROD-004', 'Same Day',       20, 6.99,  0.00, 0.30)
) AS v(order_id, order_date_sk, ship_date_sk, customer_id, product_id,
       ship_mode, quantity, unit_price, discount, margin)
JOIN dim_customer c ON c.customer_id = v.customer_id
JOIN dim_product  p ON p.product_id  = v.product_id
ON CONFLICT DO NOTHING;

-- ── Materialized View refresh ──────────────────────────────────────────────
REFRESH MATERIALIZED VIEW mv_monthly_revenue;
REFRESH MATERIALIZED VIEW mv_customer_summary;