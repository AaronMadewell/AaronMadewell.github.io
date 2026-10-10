# Data dictionary (schema v1.1)

## suppliers
| Column | Type and rules | Meaning |
|---|---|---|
| supplier_id | INTEGER, PK | Unique supplier |
| name | TEXT, required | Supplier name |
| lead_time_days | INTEGER, required | Days from order to delivery |

## products
| Column | Type and rules | Meaning |
|---|---|---|
| product_id | INTEGER, PK | Unique product |
| sku | TEXT, unique, required | Product code |
| name | TEXT, required | Product name |
| category | TEXT, required | Reporting category |
| unit_cost | REAL, required | What we pay per unit |
| unit_price | REAL, required | What we charge per unit |
| reorder_point | INTEGER, required | Reorder when stock is at or below this |
| supplier_id | INTEGER, FK suppliers | Primary supplier |

## inventory
| Column | Type and rules | Meaning |
|---|---|---|
| product_id | INTEGER, PK, FK products | One stock row per product |
| on_hand | INTEGER, CHECK >= 0 | Units in stock |

## customers
| Column | Type and rules | Meaning |
|---|---|---|
| customer_id | INTEGER, PK | Unique customer |
| name | TEXT, required | Customer name |
| region | TEXT, required | North, South or West |

## orders
| Column | Type and rules | Meaning |
|---|---|---|
| order_id | INTEGER, PK | Unique order |
| customer_id | INTEGER, FK customers | Who ordered |
| order_date | TEXT, required | ISO date |
| status | TEXT, CHECK | Placed, Picked, Shipped, Delivered or Cancelled |
| shipped_date | TEXT | Required for Shipped and Delivered; empty otherwise |

## order_items
| Column | Type and rules | Meaning |
|---|---|---|
| order_id | INTEGER, PK part, FK orders | Which order |
| product_id | INTEGER, PK part, FK products | Which product |
| qty | INTEGER, CHECK > 0 | Units ordered |

