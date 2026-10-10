-- Q1 Products at or below reorder point (replenishment list), with supplier lead time
SELECT p.sku, p.name, i.on_hand, p.reorder_point, s.name AS supplier, s.lead_time_days
FROM products p JOIN inventory i ON i.product_id = p.product_id JOIN suppliers s ON s.supplier_id = p.supplier_id
WHERE i.on_hand <= p.reorder_point ORDER BY (p.reorder_point - i.on_hand) DESC;

-- Q2 Revenue and gross margin by category (excluding cancelled orders)
SELECT p.category, SUM(oi.qty * p.unit_price) AS revenue,
       ROUND(100.0 * SUM(oi.qty * (p.unit_price - p.unit_cost)) / SUM(oi.qty * p.unit_price), 1) AS margin_pct
FROM order_items oi JOIN orders o ON o.order_id = oi.order_id JOIN products p ON p.product_id = oi.product_id
WHERE o.status <> 'Cancelled' GROUP BY p.category ORDER BY revenue DESC;

-- Q3 Average days from order to shipment by region (shipped/delivered orders only)
SELECT c.region, COUNT(*) AS orders, ROUND(AVG(julianday(o.shipped_date) - julianday(o.order_date)), 1) AS avg_days_to_ship
FROM orders o JOIN customers c ON c.customer_id = o.customer_id WHERE o.shipped_date IS NOT NULL
GROUP BY c.region ORDER BY avg_days_to_ship DESC;

-- Q4 Open orders that cannot be fully filled from current stock (data-quality / fulfillment risk)
SELECT o.order_id, c.name AS customer, p.sku, oi.qty AS ordered, i.on_hand
FROM orders o JOIN customers c ON c.customer_id = o.customer_id JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id JOIN inventory i ON i.product_id = p.product_id
WHERE o.status IN ('Placed','Picked') AND oi.qty > i.on_hand;

-- Q5 Top customers by revenue with share of total
WITH rev AS (SELECT c.name, SUM(oi.qty * p.unit_price) AS revenue FROM orders o JOIN customers c ON c.customer_id = o.customer_id
  JOIN order_items oi ON oi.order_id = o.order_id JOIN products p ON p.product_id = oi.product_id WHERE o.status <> 'Cancelled' GROUP BY c.name)
SELECT name, revenue, ROUND(100.0 * revenue / (SELECT SUM(revenue) FROM rev), 1) AS pct_of_total FROM rev ORDER BY revenue DESC;
