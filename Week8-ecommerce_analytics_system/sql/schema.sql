
-- E-Commerce Analytics Database Schema

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- Customers

CREATE TABLE customers (

    customer_id INTEGER PRIMARY KEY,

    customer_name TEXT NOT NULL,

    email TEXT,

    registration_date DATE,

    customer_type TEXT,

    city TEXT,

    state TEXT,

    region TEXT
);

-- Products

CREATE TABLE products (

    product_id INTEGER PRIMARY KEY,

    product_name TEXT NOT NULL,

    category TEXT,

    subcategory TEXT,

    brand TEXT,

    cost_price REAL,

    selling_price REAL,

    rating REAL
);

-- Orders

CREATE TABLE orders (

    order_id INTEGER PRIMARY KEY,

    customer_id INTEGER,

    order_date DATETIME,

    status TEXT,

    payment_method TEXT,

    shipping_cost REAL,

    region TEXT,

    FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id)
);

-- Order Items

CREATE TABLE order_items (

    item_id INTEGER PRIMARY KEY,

    order_id INTEGER,

    product_id INTEGER,

    quantity INTEGER,

    unit_price REAL,

    discount_percent REAL,

    FOREIGN KEY(order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY(product_id)
        REFERENCES products(product_id)
);