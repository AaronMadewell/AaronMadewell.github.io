-- Practice sample: Inventory & Order Tracking (hypothetical small retailer). Not employer data.
-- Schema v1.1. Run PRAGMA foreign_keys = ON on every connection (fixes D-002: SQLite does not enforce foreign keys by default).
PRAGMA foreign_keys = ON;
CREATE TABLE suppliers (supplier_id INTEGER PRIMARY KEY, name TEXT NOT NULL, lead_time_days INTEGER NOT NULL);
CREATE TABLE products (product_id INTEGER PRIMARY KEY, sku TEXT UNIQUE NOT NULL, name TEXT NOT NULL, category TEXT NOT NULL,
  unit_cost REAL NOT NULL, unit_price REAL NOT NULL, reorder_point INTEGER NOT NULL, supplier_id INTEGER NOT NULL REFERENCES suppliers(supplier_id));
CREATE TABLE inventory (product_id INTEGER PRIMARY KEY REFERENCES products(product_id), on_hand INTEGER NOT NULL CHECK (on_hand >= 0));
CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name TEXT NOT NULL, region TEXT NOT NULL);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
  order_date TEXT NOT NULL, status TEXT NOT NULL CHECK (status IN ('Placed','Picked','Shipped','Delivered','Cancelled')), shipped_date TEXT,
  -- v1.1 (fixes D-001): shipped and delivered orders must have a ship date; all other statuses must not
  CHECK ((status IN ('Shipped','Delivered') AND shipped_date IS NOT NULL) OR (status NOT IN ('Shipped','Delivered') AND shipped_date IS NULL)));
CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(order_id), product_id INTEGER NOT NULL REFERENCES products(product_id),
  qty INTEGER NOT NULL CHECK (qty > 0), PRIMARY KEY (order_id, product_id));
