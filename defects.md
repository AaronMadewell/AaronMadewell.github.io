# Defect log

Found by running test cases T01 to T15 (run_uat.py) against my first schema (v1.0).

| ID | Found by | Severity | Description | Root cause | Fix | Retest |
|---|---|---|---|---|---|---|
| D-001 | T14 (US-12) | Medium | An order could be saved as Shipped with no ship date, which would silently drop it from the shipping-time report. | The schema checked status values but not the link between status and ship date. | v1.1 adds a CHECK: Shipped and Delivered require a ship date; other statuses require none. | PASS in v1.1 |
| D-002 | T06 (US-05) | High | A line item for a product that does not exist was accepted. | SQLite does not enforce foreign keys unless PRAGMA foreign_keys = ON is set on each connection. | v1.1 sets the pragma in the schema file and the requirement is recorded: every connection must enable it. | PASS in v1.1 (and in v1.0 once the pragma is on) |
