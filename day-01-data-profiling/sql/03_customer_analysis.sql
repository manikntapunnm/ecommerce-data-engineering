-- =====================================================
-- DAY 01 - CUSTOMER ANALYSIS
-- =====================================================

-- 1. Total unique customers
SELECT
    COUNT(DISTINCT customer_id) AS total_customers
FROM ecommerce;


-- 2. Orders per customer
SELECT
    customer_id,
    customer_name,
    COUNT(*) AS total_orders
FROM ecommerce
GROUP BY customer_id, customer_name
ORDER BY total_orders DESC;


-- 3. Customer quantity purchased
SELECT
    customer_id,
    customer_name,
    SUM(quantity) AS total_quantity
FROM ecommerce
GROUP BY customer_id, customer_name
ORDER BY total_quantity DESC;


-- 4. Customer spending
SELECT
    customer_id,
    customer_name,
    ROUND(
        SUM(quantity * unit_price * (1 - discount / 100.0)),
        2
    ) AS total_spending
FROM ecommerce
GROUP BY customer_id, customer_name
ORDER BY total_spending DESC;


-- 5. Average order value by customer
SELECT
    customer_id,
    customer_name,
    ROUND(
        SUM(quantity * unit_price * (1 - discount / 100.0))
        / COUNT(*),
        2
    ) AS average_order_value
FROM ecommerce
GROUP BY customer_id, customer_name
ORDER BY average_order_value DESC;

