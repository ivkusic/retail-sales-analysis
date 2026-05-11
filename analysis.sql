DROP TABLE IF EXISTS superstore;

CREATE TABLE IF NOT EXISTS superstore (
    row_id          INTEGER,
    order_id        TEXT,
    order_date      TEXT,
    ship_date       TEXT,
    ship_mode       TEXT,
    customer_id     TEXT,
    customer_name   TEXT,
    segment         TEXT,
    country         TEXT,
    city            TEXT,
    state           TEXT,
    postal_code     TEXT,
    region          TEXT,
    product_id      TEXT,
    category        TEXT,
    sub_category    TEXT,
    product_name    TEXT,
    sales           REAL,
    quantity        INTEGER,
    discount        REAL,
    profit          REAL,
    profit_margin   REAL,
    days_to_ship    INTEGER
);


-- Total Sales and Profit by Region
SELECT
    region,
    ROUND(SUM(sales), 2)          AS total_sales,
    ROUND(SUM(profit), 2)         AS total_profit,
    ROUND(AVG(profit_margin), 2)  AS avg_profit_margin_pct,
    COUNT(DISTINCT order_id)      AS order_count
FROM superstore
GROUP BY region
ORDER BY total_sales DESC;


-- Top 10 Products by Sales
SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2)   AS total_sales,
    ROUND(SUM(profit), 2)  AS total_profit,
    SUM(quantity)          AS units_sold
FROM superstore
GROUP BY product_name, category, sub_category
ORDER BY total_sales DESC
LIMIT 10;


-- Monthly Sales Trend
SELECT
    SUBSTR(order_date, 1, 7)   AS year_month,
    ROUND(SUM(sales), 2)       AS monthly_sales,
    ROUND(SUM(profit), 2)      AS monthly_profit,
    COUNT(DISTINCT order_id)   AS orders
FROM superstore
GROUP BY year_month
ORDER BY year_month;


-- Sales and Profit by Category and Sub-Category
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 2)          AS total_sales,
    ROUND(SUM(profit), 2)         AS total_profit,
    ROUND(AVG(profit_margin), 2)  AS avg_profit_margin_pct,
    SUM(quantity)                 AS units_sold
FROM superstore
GROUP BY category, sub_category
ORDER BY category, total_sales DESC;


-- Average Discount by Customer Segment
SELECT
    segment,
    ROUND(AVG(discount) * 100, 2)  AS avg_discount_pct,
    ROUND(SUM(sales), 2)           AS total_sales,
    ROUND(SUM(profit), 2)          AS total_profit,
    COUNT(DISTINCT customer_id)    AS unique_customers
FROM superstore
GROUP BY segment
ORDER BY avg_discount_pct DESC;


-- Top 5 States by Profit
SELECT
    state,
    region,
    ROUND(SUM(profit), 2)          AS total_profit,
    ROUND(SUM(sales), 2)           AS total_sales,
    ROUND(AVG(profit_margin), 2)   AS avg_profit_margin_pct,
    COUNT(DISTINCT order_id)       AS order_count
FROM superstore
GROUP BY state, region
ORDER BY total_profit DESC
LIMIT 5;
