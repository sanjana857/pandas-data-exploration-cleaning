-- Query 1
-- Total Revenue by Category

SELECT

    p.category,

    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_revenue

FROM order_items oi

JOIN products p

ON oi.product_id = p.product_id

GROUP BY p.category

ORDER BY total_revenue DESC;

-- Query 2
-- Top 10 Customers

SELECT

    c.customer_id,

    c.customer_name,

    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_spending

FROM customers c

JOIN orders o

ON c.customer_id = o.customer_id

JOIN order_items oi

ON o.order_id = oi.order_id

GROUP BY

c.customer_id,
c.customer_name

ORDER BY total_spending DESC

LIMIT 10;


-- Query 3
-- Revenue by Month

SELECT

strftime('%Y-%m', order_date) AS month,

ROUND(

SUM(

quantity *

unit_price *

(1-discount_percent/100.0)

),

2

) AS revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY month

ORDER BY month;


-- Query 4
-- Top Products

SELECT

p.product_name,

SUM(oi.quantity) total_quantity,

ROUND(

SUM(

oi.quantity*

oi.unit_price*

(1-oi.discount_percent/100.0)

),

2

) revenue

FROM products p

JOIN order_items oi

ON p.product_id=oi.product_id

GROUP BY p.product_name

ORDER BY revenue DESC

LIMIT 10;


-- Query 5
-- Average Order Value

SELECT

ROUND(

AVG(order_total),

2

) average_order_value

FROM

(

SELECT

order_id,

SUM(

quantity*

unit_price*

(1-discount_percent/100.0)

) order_total

FROM order_items

GROUP BY order_id

);

-- Query 6
-- Month-wise Order Count (Last 12 Months)

SELECT

strftime('%Y-%m',order_date) AS month,

COUNT(order_id) AS total_orders

FROM orders

WHERE order_date >= date('now','-12 months')

GROUP BY month

ORDER BY month;