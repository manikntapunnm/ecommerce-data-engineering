/*
======================================================================
DAY 2 - CLEAN DATA POSTGRESQL VALIDATION
======================================================================

Purpose:
    Validate the cleaned e-commerce dataset in PostgreSQL.

Source:
    data/processed/ecommerce_clean.csv

Target table:
    ecommerce_clean

The original Day 1 table "ecommerce" is not modified.
*/


-- ====================================================================
-- 1. Disable pager
-- ====================================================================

\pset pager off


-- ====================================================================
-- 2. Drop previous Day 2 validation table
-- ====================================================================

DROP TABLE IF EXISTS ecommerce_clean;


-- ====================================================================
-- 3. Create cleaned-data table
-- ====================================================================

CREATE TABLE ecommerce_clean (
    order_id INTEGER PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id INTEGER NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    product_id INTEGER NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    discount NUMERIC(5,2) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    gross_amount NUMERIC(18,2) NOT NULL,
    discount_amount NUMERIC(18,2) NOT NULL,
    net_amount NUMERIC(18,2) NOT NULL
);


-- -- ====================================================================
-- -- 4. Load cleaned CSV
-- -- ====================================================================

-- \copy ecommerce_clean (
--     order_id,
--     order_date,
--     customer_id,
--     customer_name,
--     product_id,
--     product_name,
--     category,
--     quantity,
--     unit_price,
--     discount,
--     city,
--     state,
--     country,
--     payment_method,
--     gross_amount,
--     discount_amount,
--     net_amount
-- )
-- FROM 'C:/Users/Durga/Desktop/ecommerce-data-engineering/data/processed/ecommerce_clean.csv'
-- WITH (
--     FORMAT csv,
--     HEADER true
-- );
-- ====================================================================
-- 4. Load cleaned CSV
-- ====================================================================

\copy ecommerce_clean FROM 'C:/Users/Durga/Desktop/ecommerce-data-engineering/data/processed/ecommerce_clean.csv' WITH (FORMAT csv, HEADER true)


-- ====================================================================
-- 5. Row count validation
-- ====================================================================

SELECT
    COUNT(*) AS total_rows
FROM ecommerce_clean;


-- ====================================================================
-- 6. Column structure
-- ====================================================================

SELECT
    column_name,
    data_type,
    numeric_precision,
    numeric_scale
FROM information_schema.columns
WHERE table_name = 'ecommerce_clean'
ORDER BY ordinal_position;


-- ====================================================================
-- 7. Duplicate order ID validation
-- ====================================================================

SELECT
    COUNT(*) AS duplicate_order_ids
FROM (
    SELECT
        order_id
    FROM ecommerce_clean
    GROUP BY order_id
    HAVING COUNT(*) > 1
) duplicates;


-- ====================================================================
-- 8. Missing-value validation
-- ====================================================================

SELECT
    COUNT(*) FILTER (WHERE order_id IS NULL) AS missing_order_id,
    COUNT(*) FILTER (WHERE order_date IS NULL) AS missing_order_date,
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS missing_customer_id,
    COUNT(*) FILTER (WHERE product_id IS NULL) AS missing_product_id,
    COUNT(*) FILTER (WHERE quantity IS NULL) AS missing_quantity,
    COUNT(*) FILTER (WHERE unit_price IS NULL) AS missing_unit_price,
    COUNT(*) FILTER (WHERE discount IS NULL) AS missing_discount,
    COUNT(*) FILTER (WHERE gross_amount IS NULL) AS missing_gross_amount,
    COUNT(*) FILTER (WHERE discount_amount IS NULL) AS missing_discount_amount,
    COUNT(*) FILTER (WHERE net_amount IS NULL) AS missing_net_amount
FROM ecommerce_clean;


-- ====================================================================
-- 9. Business-rule validation
-- ====================================================================

SELECT
    COUNT(*) FILTER (WHERE order_id <= 0) AS invalid_order_ids,
    COUNT(*) FILTER (WHERE customer_id <= 0) AS invalid_customer_ids,
    COUNT(*) FILTER (WHERE product_id <= 0) AS invalid_product_ids,
    COUNT(*) FILTER (WHERE quantity <= 0) AS invalid_quantities,
    COUNT(*) FILTER (WHERE unit_price < 0) AS invalid_unit_prices,
    COUNT(*) FILTER (
        WHERE discount < 0 OR discount > 100
    ) AS invalid_discounts,
    COUNT(*) FILTER (WHERE gross_amount < 0) AS negative_gross_amounts,
    COUNT(*) FILTER (WHERE discount_amount < 0) AS negative_discount_amounts,
    COUNT(*) FILTER (WHERE net_amount < 0) AS negative_net_amounts
FROM ecommerce_clean;


-- ====================================================================
-- 10. Validate calculated gross amount
-- ====================================================================

SELECT
    COUNT(*) AS incorrect_gross_amounts
FROM ecommerce_clean
WHERE gross_amount !=
      ROUND(quantity * unit_price, 2);



-- ====================================================================
-- 11. Validate calculated discount amount
-- ====================================================================

SELECT
    COUNT(*) AS incorrect_discount_amounts
FROM ecommerce_clean
WHERE discount_amount !=
      ROUND(
          ROUND(quantity * unit_price, 2)
          * discount
          / 100.0,
          2
      );

-- ====================================================================
-- 12. Validate calculated net amount
-- ====================================================================

SELECT
    COUNT(*) AS incorrect_net_amounts
FROM ecommerce_clean
WHERE net_amount !=
      ROUND(
          ROUND(quantity * unit_price, 2)
          -
          ROUND(
              ROUND(quantity * unit_price, 2)
              * discount
              / 100.0,
              2
          ),
          2
      );

-- ====================================================================
-- 13. Clean transaction revenue
-- ====================================================================

SELECT
    SUM(net_amount) AS rounded_transaction_revenue
FROM ecommerce_clean;


-- ====================================================================
-- 14. Business-formula revenue
-- ====================================================================

SELECT
    ROUND(
        SUM(
            quantity
            * unit_price
            * (1 - discount / 100.0)
        ),
        2
    ) AS calculated_revenue
FROM ecommerce_clean;


-- ====================================================================
-- 15. Compare with Day 1 revenue
-- ====================================================================

SELECT
    ROUND(
        SUM(
            quantity
            * unit_price
            * (1 - discount / 100.0)
        ),
        2
    ) AS day_2_revenue,
    214366057.77 AS day_1_revenue,
    ROUND(
        SUM(
            quantity
            * unit_price
            * (1 - discount / 100.0)
        ),
        2
    ) - 214366057.77 AS difference
FROM ecommerce_clean;


-- ====================================================================
-- 16. Summary statistics
-- ====================================================================

SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT product_id) AS total_products,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(gross_amount), 2) AS total_gross_amount,
    ROUND(SUM(discount_amount), 2) AS total_discount_amount,
    ROUND(
        SUM(
            quantity
            * unit_price
            * (1 - discount / 100.0)
        ),
        2
    ) AS total_net_revenue
FROM ecommerce_clean;