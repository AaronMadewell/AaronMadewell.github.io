# Traceability: story to test to result

| Story | Test | Scenario | v1.0 (default) | v1.0 (FK on) | v1.1 (FK on) |
|---|---|---|---|---|---|
| US-01 | T01 | Enter an order with one line item | PASS | PASS | PASS |
| US-02 | T02 | Reject a line item with quantity 0 | PASS | PASS | PASS |
| US-02 | T03 | Reject a line item with negative quantity | PASS | PASS | PASS |
| US-03 | T04 | Reject an invalid order status ('Lost') | PASS | PASS | PASS |
| US-04 | T05 | Reject a duplicate product code (SKU) | PASS | PASS | PASS |
| US-05 | T06 | Reject a line item for a product that does not exist | FAIL | PASS | PASS |
| US-06 | T07 | Block a pick that exceeds on-hand stock | PASS | PASS | PASS |
| US-07 | T08 | Picking 12 units reduces stock by 12 | PASS | PASS | PASS |
| US-08 | T09 | Reorder list matches an independent calculation | PASS | PASS | PASS |
| US-09 | T10 | A product that falls to its reorder point appears on the list | PASS | PASS | PASS |
| US-10 | T11 | Revenue by category excludes cancelled orders and matches Python | PASS | PASS | PASS |
| US-10 | T12 | Gross margin percent matches Python | PASS | PASS | PASS |
| US-11 | T13 | Days-to-ship counts only shipped or delivered orders | PASS | PASS | PASS |
| US-12 | T14 | Reject a 'Shipped' order that has no ship date | FAIL | FAIL | PASS |
| US-01 | T15 | Reject the same product twice on one order | PASS | PASS | PASS |

Totals: v1.0 default 13/15; v1.0 with foreign keys on 14/15; v1.1 15/15.
