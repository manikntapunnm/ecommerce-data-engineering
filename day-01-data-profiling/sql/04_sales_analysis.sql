-- =====================================================
-- DAY 01 - SALES ANALYSIS
-- =====================================================

-- 1. Total revenue
SELECT
    ROUND(
        SUM(quantity * unit_price * (1 - discount / 100.0)),
        2
    ) AS total_revenue
FROM ecommerce;


-- 2. Total quantity sold
SELECT
    SUM(quantity) AS total_quantity_sold
FROM ecommerce;


-- 3. Total orders
SELECT
    COUNT(*) AS total_orders
FROM ecommerce;


-- 4. Average order value
SELECT
    ROUND(
        SUM(quantity * unit_price * (1 - discount / 100.0))
        / COUNT(*),
        2
    ) AS average_order_value
FROM ecommerce;


-- 5. Revenue by category
SELECT
    category,
    ROUND(
        SUM(quantity * unit_price * (1 - discount / 100.0)),
        2
    ) AS revenue
FROM ecommerce
GROUP BY category
ORDER BY revenue DESC;


-- 6. Revenue by product
SELECT
    product_id,
    product_name,
    ROUND(
        SUM(quantity * unit_price * (1 - discount / 100.0)),
        2
    ) AS revenue
FROM ecommerce
GROUP BY product_id, product_name
ORDER BY revenue DESC;


-- 7. Monthly revenue
SELECT
    DATE_TRUNC('month', order_date)::DATE AS month,
    ROUND(
        SUM(quantity * unit_price * (1 - discount / 100.0)),
        2
    ) AS revenue
FROM ecommerce
GROUP BY month
ORDER BY month;


-- 8. Revenue by state
SELECT
    state,
    ROUND(
        SUM(quantity * unit_price * (1 - discount / 100.0)),
        2
    ) AS revenue
FROM ecommerce
GROUP BY state
ORDER BY revenue DESC;


-- 9. Revenue by payment method
SELECT
    payment_method,
    ROUND(
        SUM(quantity * unit_price * (1 - discount / 100.0)),
        2
    ) AS revenue
FROM ecommerce
GROUP BY payment_method
ORDER BY revenue DESC;

