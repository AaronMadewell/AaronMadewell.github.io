# User stories and acceptance criteria

Practice sample with hypothetical data. Format: Given / When / Then.

## US-01 Enter an order
- **Story:** As an order clerk, I want to enter an order once with its line items so nothing is retyped.
- **Acceptance criteria:** Given a customer and in-stock products, When I save an order with line items, Then the order and every line item are stored, and the same product cannot appear twice on one order.
- **Priority (MoSCoW):** Must
- **Traces to requirement:** FR1

## US-02 Reject bad quantities
- **Story:** As an order clerk, I want zero or negative quantities rejected so bad data never enters the system.
- **Acceptance criteria:** Given an order, When I add a line item with quantity 0 or less, Then the system rejects it.
- **Priority (MoSCoW):** Must
- **Traces to requirement:** FR1

## US-03 Allow only valid statuses
- **Story:** As the operations manager, I want orders to use only agreed statuses so reports are reliable.
- **Acceptance criteria:** Given an order, When I set a status other than Placed, Picked, Shipped, Delivered or Cancelled, Then the system rejects it.
- **Priority (MoSCoW):** Must
- **Traces to requirement:** FR1

## US-04 Unique product codes
- **Story:** As purchasing, I want each product code to be unique so I never order the wrong item.
- **Acceptance criteria:** Given an existing product code, When I add another product with the same code, Then the system rejects it.
- **Priority (MoSCoW):** Must
- **Traces to requirement:** FR1

## US-05 Valid references only
- **Story:** As the operations manager, I want every line item to point to a real product and order.
- **Acceptance criteria:** Given a line item for a product that does not exist, When I save it, Then the system rejects it.
- **Priority (MoSCoW):** Must
- **Traces to requirement:** FR1

## US-06 Block over-picking
- **Story:** As a picker, I want a pick blocked when it exceeds stock so counts never go negative.
- **Acceptance criteria:** Given 35 units on hand, When I pick 500, Then the pick is rejected and stock stays at 35 and the shortfall is shown.
- **Priority (MoSCoW):** Must
- **Traces to requirement:** FR2

## US-07 Stock falls on pick
- **Story:** As a picker, I want stock to drop when I pick so counts stay accurate.
- **Acceptance criteria:** Given 60 units on hand, When I pick 12, Then on-hand becomes 48.
- **Priority (MoSCoW):** Must
- **Traces to requirement:** FR2

## US-08 Daily reorder list
- **Story:** As purchasing, I want a daily list of products at or below reorder point with supplier and lead time so I order in time.
- **Acceptance criteria:** Given stock levels, When I open the reorder list, Then it shows every product at or below its reorder point, with supplier and lead time, largest shortfall first.
- **Priority (MoSCoW):** Must
- **Traces to requirement:** FR3

## US-09 List updates with stock
- **Story:** As purchasing, I want the list to update when stock changes so I see new shortages.
- **Acceptance criteria:** Given a product above its reorder point, When a pick brings it to the reorder point, Then it appears on the next list.
- **Priority (MoSCoW):** Should
- **Traces to requirement:** FR3

## US-10 Revenue and margin report
- **Story:** As finance, I want revenue and margin by category so I can see what drives profit.
- **Acceptance criteria:** Given orders in any status, When I run the report, Then cancelled orders are excluded and margin percent equals (price minus cost) divided by price, to one decimal.
- **Priority (MoSCoW):** Must
- **Traces to requirement:** FR4

## US-11 Shipping time by region
- **Story:** As the operations manager, I want average days to ship by region so I can find slow lanes.
- **Acceptance criteria:** Given orders with ship dates, When I run the report, Then only shipped or delivered orders are counted, with order count and average days per region.
- **Priority (MoSCoW):** Should
- **Traces to requirement:** FR5

## US-12 Ship dates on shipped orders
- **Story:** As the operations manager, I want shipped orders to have a ship date so the shipping report is complete.
- **Acceptance criteria:** Given an order marked Shipped or Delivered, When I save it without a ship date, Then the system rejects it.
- **Priority (MoSCoW):** Must
- **Traces to requirement:** FR5

