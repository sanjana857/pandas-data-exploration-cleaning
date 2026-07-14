-- Query 1
-- Customer Cohort Analysis

WITH FirstPurchase AS (

    SELECT
        customer_id,
        MIN(strftime('%Y-%m', order_date)) AS cohort_month
    FROM orders
    WHERE customer_id IS NOT NULL
    GROUP BY customer_id

),

CustomerActivity AS (

    SELECT
        customer_id,
        strftime('%Y-%m', order_date) AS order_month
    FROM orders
    WHERE customer_id IS NOT NULL

)

SELECT
    fp.cohort_month,
    ca.order_month,
    COUNT(DISTINCT ca.customer_id) AS active_customers

FROM FirstPurchase fp

JOIN CustomerActivity ca
ON fp.customer_id = ca.customer_id

GROUP BY
fp.cohort_month,
ca.order_month

ORDER BY
fp.cohort_month,
ca.order_month;

-- Query 1
-- Customer Cohort Analysis

WITH FirstPurchase AS (

    SELECT
        customer_id,
        MIN(strftime('%Y-%m', order_date)) AS cohort_month
    FROM orders
    WHERE customer_id IS NOT NULL
    GROUP BY customer_id

),

CustomerActivity AS (

    SELECT
        customer_id,
        strftime('%Y-%m', order_date) AS order_month
    FROM orders
    WHERE customer_id IS NOT NULL

)

SELECT
    fp.cohort_month,
    ca.order_month,
    COUNT(DISTINCT ca.customer_id) AS active_customers

FROM FirstPurchase fp

JOIN CustomerActivity ca
ON fp.customer_id = ca.customer_id

GROUP BY
fp.cohort_month,
ca.order_month

ORDER BY
fp.cohort_month,
ca.order_month;

-- Query 2
-- Repeat Customers

SELECT

customer_id,

COUNT(order_id) total_orders,

CASE

WHEN COUNT(order_id)=1

THEN 'One Time'

WHEN COUNT(order_id)<=5

THEN 'Occasional'

ELSE 'Loyal'

END customer_segment

FROM orders

WHERE customer_id IS NOT NULL

GROUP BY customer_id

ORDER BY total_orders DESC;

-- Query 3
-- Spend Tier

WITH CustomerRevenue AS (

SELECT

c.customer_id,

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

c.customer_id,

c.customer_name

)

SELECT

customer_id,

customer_name,

ROUND(revenue,2),

CASE

WHEN revenue<5000 THEN 'Low'

WHEN revenue<15000 THEN 'Medium'

ELSE 'High'

END spend_tier

FROM CustomerRevenue

ORDER BY revenue DESC;

-- Query 4
-- RFM Analysis

WITH CustomerMetrics AS (

SELECT

o.customer_id,

MAX(order_date) last_order,

COUNT(DISTINCT o.order_id) frequency,

SUM(

oi.quantity*
oi.unit_price*
(1-oi.discount_percent/100.0)

)

monetary

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

WHERE customer_id IS NOT NULL

GROUP BY customer_id

)

SELECT

customer_id,

last_order,

frequency,

ROUND(monetary,2)

FROM CustomerMetrics

ORDER BY monetary DESC;

-- Query 5
-- NTILE Segmentation

WITH Revenue AS (

SELECT

o.customer_id,

SUM(

oi.quantity*
oi.unit_price*
(1-oi.discount_percent/100.0)

)

revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

WHERE customer_id IS NOT NULL

GROUP BY customer_id

)

SELECT

customer_id,

ROUND(revenue,2),

NTILE(4)

OVER(

ORDER BY revenue DESC

)

quartile

FROM Revenue;

-- Query 6
-- Year over Year Revenue

WITH Revenue AS (

SELECT

strftime('%Y',order_date) year,

strftime('%m',order_date) month,

SUM(

oi.quantity*
oi.unit_price*
(1-oi.discount_percent/100.0)

)

revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY year,month

)

SELECT *

FROM Revenue

ORDER BY year,month;

-- Query 7
-- Frequently Bought Together

SELECT

a.product_id product_a,

b.product_id product_b,

COUNT(*) times_bought_together

FROM order_items a

JOIN order_items b

ON a.order_id=b.order_id

AND a.product_id<b.product_id

GROUP BY

a.product_id,

b.product_id

ORDER BY times_bought_together DESC

LIMIT 20;


-- First Purchased Category

WITH CustomerCategory AS (

SELECT

o.customer_id,

p.category,

o.order_date,

ROW_NUMBER()

OVER(

PARTITION BY o.customer_id

ORDER BY o.order_date

)

rn

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

JOIN products p

ON oi.product_id=p.product_id

)

SELECT

customer_id,

category

FROM CustomerCategory

WHERE rn=1;


-- Most Recent Category

WITH CustomerCategory AS (

SELECT

o.customer_id,

p.category,

o.order_date,

ROW_NUMBER()

OVER(

PARTITION BY o.customer_id

ORDER BY o.order_date DESC

)

rn

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

JOIN products p

ON oi.product_id=p.product_id

)

SELECT

customer_id,

category

FROM CustomerCategory

WHERE rn=1;

-- Query 8
-- First Purchased Category vs Most Recent Purchased Category


WITH CustomerPurchaseHistory AS (

    SELECT
        o.customer_id,
        p.category,
        o.order_date,

        ROW_NUMBER() OVER (
            PARTITION BY o.customer_id
            ORDER BY o.order_date ASC
        ) AS first_order,

        ROW_NUMBER() OVER (
            PARTITION BY o.customer_id
            ORDER BY o.order_date DESC
        ) AS last_order

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    WHERE o.customer_id IS NOT NULL

),

FirstCategory AS (

    SELECT
        customer_id,
        category AS first_category
    FROM CustomerPurchaseHistory
    WHERE first_order = 1

),

LastCategory AS (

    SELECT
        customer_id,
        category AS last_category
    FROM CustomerPurchaseHistory
    WHERE last_order = 1

)

SELECT

    f.customer_id,

    f.first_category,

    l.last_category,

    CASE

        WHEN f.first_category = l.last_category

        THEN 'No'

        ELSE 'Yes'

    END AS category_shift

FROM FirstCategory f

JOIN LastCategory l

ON f.customer_id = l.customer_id

ORDER BY f.customer_id;


-- Query 9
-- Cumulative Revenue Distribution

WITH CustomerRevenue AS (

    SELECT

        o.customer_id,

        ROUND(

            SUM(

                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent / 100.0)

            ),

            2

        ) AS revenue

    FROM orders o

    JOIN order_items oi

        ON o.order_id = oi.order_id

    WHERE o.customer_id IS NOT NULL

    GROUP BY o.customer_id

),

RevenueDistribution AS (

    SELECT

        customer_id,

        revenue,

        SUM(revenue) OVER (

            ORDER BY revenue DESC

        ) AS cumulative_revenue,

        SUM(revenue) OVER () AS total_revenue

    FROM CustomerRevenue

)

SELECT

    customer_id,

    revenue,

    cumulative_revenue,

    ROUND(

        (cumulative_revenue * 100.0) / total_revenue,

        2

    ) AS cumulative_percent

FROM RevenueDistribution

ORDER BY revenue DESC;


-- Query 10
-- Multi-Level CTE : Monthly Revenue & Customer Segmentation

WITH MonthlyCustomerRevenue AS (

    SELECT

        strftime('%Y-%m', o.order_date) AS order_month,

        o.customer_id,

        ROUND(

            SUM(

                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent / 100.0)

            ),

            2

        ) AS monthly_revenue

    FROM orders o

    JOIN order_items oi

        ON o.order_id = oi.order_id

    WHERE o.customer_id IS NOT NULL

    GROUP BY

        order_month,

        o.customer_id

),

CustomerCategory AS (

    SELECT

        order_month,

        customer_id,

        monthly_revenue,

        CASE

            WHEN monthly_revenue > 10000

                THEN 'High'

            WHEN monthly_revenue >= 5000

                THEN 'Medium'

            ELSE 'Low'

        END AS customer_category

    FROM MonthlyCustomerRevenue

)

SELECT

    order_month,

    customer_category,

    COUNT(customer_id) AS total_customers

FROM CustomerCategory

GROUP BY

    order_month,

    customer_category

ORDER BY

    order_month,

    customer_category;


-- Query 11
-- Customer Cohort Retention Analysis


WITH CustomerFirstOrder AS (

    SELECT

        customer_id,

        MIN(DATE(order_date)) AS first_order_date

    FROM orders

    WHERE customer_id IS NOT NULL

    GROUP BY customer_id

),

CustomerOrders AS (

    SELECT

        o.customer_id,

        DATE(o.order_date) AS order_date,

        strftime('%Y-%m', f.first_order_date) AS cohort_month,

        (
            (CAST(strftime('%Y', o.order_date) AS INTEGER) -
             CAST(strftime('%Y', f.first_order_date) AS INTEGER)) * 12
            +
            (CAST(strftime('%m', o.order_date) AS INTEGER) -
             CAST(strftime('%m', f.first_order_date) AS INTEGER))
        ) AS month_number

    FROM orders o

    JOIN CustomerFirstOrder f

    ON o.customer_id = f.customer_id

),

CohortSize AS (

    SELECT

        cohort_month,

        COUNT(DISTINCT customer_id) AS total_customers

    FROM CustomerOrders

    WHERE month_number = 0

    GROUP BY cohort_month

)

SELECT

    c.cohort_month,

    c.month_number,

    COUNT(DISTINCT c.customer_id) AS retained_customers,

    s.total_customers,

    ROUND(

        COUNT(DISTINCT c.customer_id) * 100.0 /

        s.total_customers,

        2

    ) AS retention_rate

FROM CustomerOrders c

JOIN CohortSize s

ON c.cohort_month = s.cohort_month

GROUP BY

c.cohort_month,

c.month_number

ORDER BY

c.cohort_month,

c.month_number;