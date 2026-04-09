-- ============================================================
-- queries.sql  –  Retail Sales Analysis Dashboard
-- Run these in any SQLite client, or via Python (see notebook)
-- ============================================================


-- ── 1. Total overview ────────────────────────────────────────
SELECT
    COUNT(DISTINCT order_id)          AS total_orders,
    ROUND(SUM(sales), 2)              AS total_revenue,
    ROUND(SUM(profit), 2)             AS total_profit,
    ROUND(AVG(sales), 2)              AS avg_order_value,
    ROUND(SUM(profit) / SUM(sales) * 100, 1) AS profit_margin_pct
FROM sales;


-- ── 2. Monthly revenue trend ─────────────────────────────────
SELECT
    STRFTIME('%Y-%m', order_date)     AS month,
    ROUND(SUM(sales), 2)              AS monthly_revenue,
    ROUND(SUM(profit), 2)             AS monthly_profit,
    COUNT(DISTINCT order_id)          AS orders
FROM sales
GROUP BY month
ORDER BY month;


-- ── 3. Revenue & profit by region ────────────────────────────
SELECT
    region,
    COUNT(DISTINCT order_id)          AS orders,
    ROUND(SUM(sales), 2)              AS revenue,
    ROUND(SUM(profit), 2)             AS profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 1) AS margin_pct
FROM sales
GROUP BY region
ORDER BY revenue DESC;


-- ── 4. Revenue by category & sub-category ────────────────────
SELECT
    category,
    sub_category,
    COUNT(*)                          AS num_orders,
    ROUND(SUM(sales), 2)              AS revenue,
    ROUND(SUM(profit), 2)             AS profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 1) AS margin_pct
FROM sales
GROUP BY category, sub_category
ORDER BY category, revenue DESC;


-- ── 5. Top 10 products by revenue ────────────────────────────
SELECT
    product_name,
    sub_category,
    COUNT(*)                          AS times_ordered,
    ROUND(SUM(sales), 2)              AS total_revenue,
    ROUND(SUM(profit), 2)             AS total_profit
FROM sales
GROUP BY product_name, sub_category
ORDER BY total_revenue DESC
LIMIT 10;


-- ── 6. Shipping mode breakdown ───────────────────────────────
SELECT
    ship_mode,
    COUNT(*)                          AS num_orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sales), 1) AS pct_of_orders,
    ROUND(SUM(sales), 2)              AS revenue
FROM sales
GROUP BY ship_mode
ORDER BY num_orders DESC;


-- ── 7. Impact of discount on profit margin ───────────────────
SELECT
    CASE
        WHEN discount = 0    THEN '0%  – No discount'
        WHEN discount <= 0.1 THEN '10% – Light discount'
        WHEN discount <= 0.2 THEN '20% – Moderate discount'
        WHEN discount <= 0.3 THEN '30% – Heavy discount'
        ELSE                      '40%+ – Deep discount'
    END                                       AS discount_band,
    COUNT(*)                                  AS num_orders,
    ROUND(AVG(profit / sales * 100), 1)       AS avg_margin_pct,
    ROUND(SUM(sales), 2)                      AS total_revenue
FROM sales
GROUP BY discount_band
ORDER BY discount_band;


-- ── 8. Top 10 customers by revenue ───────────────────────────
SELECT
    customer_name,
    COUNT(DISTINCT order_id)          AS orders,
    ROUND(SUM(sales), 2)              AS lifetime_value,
    ROUND(SUM(profit), 2)             AS profit_contributed
FROM sales
GROUP BY customer_name
ORDER BY lifetime_value DESC
LIMIT 10;


-- ── 9. Best cities by profit ─────────────────────────────────
SELECT
    city,
    state,
    region,
    COUNT(DISTINCT order_id)          AS orders,
    ROUND(SUM(sales), 2)              AS revenue,
    ROUND(SUM(profit), 2)             AS profit
FROM sales
GROUP BY city, state, region
ORDER BY profit DESC
LIMIT 10;


-- ── 10. Year-over-year comparison ────────────────────────────
SELECT
    STRFTIME('%Y', order_date)        AS year,
    ROUND(SUM(sales), 2)              AS revenue,
    ROUND(SUM(profit), 2)             AS profit,
    COUNT(DISTINCT order_id)          AS orders
FROM sales
GROUP BY year
ORDER BY year;
