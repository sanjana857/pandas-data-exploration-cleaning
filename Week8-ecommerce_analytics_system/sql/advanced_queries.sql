-- =====================================================
-- Query 1
-- Rank Customers by Lifetime Value
-- =====================================================

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
    ) AS lifetime_value,

    DENSE_RANK() OVER(
        ORDER BY
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) DESC
    ) AS customer_rank

FROM customers c

JOIN orders o
ON c.customer_id = o.customer_id

JOIN order_items oi
ON o.order_id = oi.order_id

GROUP BY
c.customer_id,
c.customer_name

ORDER BY customer_rank;

-- =====================================================
-- Query 2
-- Running Revenue
-- =====================================================

SELECT

DATE(o.order_date) AS order_day,

ROUND(

SUM(
oi.quantity *
oi.unit_price *
(1-oi.discount_percent/100.0)

),

2

) daily_revenue,

ROUND(

SUM(

SUM(

oi.quantity *
oi.unit_price *
(1-oi.discount_percent/100.0)

)

)

OVER(

ORDER BY DATE(o.order_date)

),

2

) running_total

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY DATE(o.order_date)

ORDER BY order_day;

-- =====================================================
-- Query 3
-- 7-Day Moving Average
-- =====================================================

WITH DailyRevenue AS

(

SELECT

DATE(order_date) day,

SUM(

oi.quantity*
oi.unit_price*
(1-oi.discount_percent/100.0)

) revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY DATE(order_date)

)

SELECT

day,

ROUND(revenue,2),

ROUND(

AVG(revenue)

OVER(

ORDER BY day

ROWS BETWEEN 6 PRECEDING

AND CURRENT ROW

),

2

)

AS moving_average

FROM DailyRevenue;

-- =====================================================
-- Query 4
-- Previous Month Revenue
-- =====================================================

WITH MonthlyRevenue AS

(

SELECT

strftime('%Y-%m',order_date) month,

SUM(

oi.quantity*
oi.unit_price*
(1-oi.discount_percent/100.0)

) revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY month

)

SELECT

month,

ROUND(revenue,2),

ROUND(

LAG(revenue)

OVER(

ORDER BY month

),

2

)

AS previous_month

FROM MonthlyRevenue;

-- =====================================================
-- Query 5
-- Monthly Revenue Growth
-- =====================================================

WITH MonthlyRevenue AS

(

SELECT

strftime('%Y-%m',order_date) month,

SUM(

oi.quantity*
oi.unit_price*
(1-oi.discount_percent/100.0)

) revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY month

),

Growth AS

(

SELECT

month,

revenue,

LAG(revenue)

OVER(

ORDER BY month

)

previous_revenue

FROM MonthlyRevenue

)

SELECT

month,

ROUND(revenue,2),

ROUND(previous_revenue,2),

ROUND(

((revenue-previous_revenue)*100.0)

/

previous_revenue,

2

)

growth_percent

FROM Growth;

-- =====================================================
-- Query 6
-- Regional Ranking
-- =====================================================

WITH CustomerRevenue AS

(

SELECT

o.region,

c.customer_name,

SUM(

oi.quantity*
oi.unit_price*
(1-oi.discount_percent/100.0)

)

revenue

FROM customers c

JOIN orders o

ON c.customer_id=o.customer_id

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY

o.region,

c.customer_name

)

SELECT

region,

customer_name,

ROUND(revenue,2),

DENSE_RANK()

OVER(

PARTITION BY region

ORDER BY revenue DESC

)

rank_in_region

FROM CustomerRevenue;


-- Query 7
-- Customers with No Delivered Orders

SELECT DISTINCT

c.customer_id,

c.customer_name

FROM customers c

JOIN orders o

ON c.customer_id=o.customer_id

WHERE c.customer_id NOT IN

(

SELECT customer_id

FROM orders

WHERE status='DELIVERED'

);


-- Query 8
-- More Returns than Purchases

SELECT

p.product_name,

SUM(

CASE

WHEN o.status='RETURNED'

THEN oi.quantity

ELSE 0

END

)

returned,

SUM(

CASE

WHEN o.status<>'RETURNED'

THEN oi.quantity

ELSE 0

END

)

purchased

FROM products p

JOIN order_items oi

ON p.product_id=oi.product_id

JOIN orders o

ON oi.order_id=o.order_id

GROUP BY p.product_name

HAVING returned>purchased;


-- Query 9
-- Return Rate Per Category

SELECT

p.category,

ROUND(

100.0*

SUM(

CASE

WHEN o.status='RETURNED'

THEN oi.quantity

ELSE 0

END

)

/

SUM(oi.quantity),

2

)

AS return_rate

FROM products p

JOIN order_items oi

ON p.product_id=oi.product_id

JOIN orders o

ON oi.order_id=o.order_id

GROUP BY p.category;