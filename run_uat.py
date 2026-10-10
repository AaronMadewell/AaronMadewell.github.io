"""UAT runner for the Inventory & Order Tracking practice database.
Usage: python run_uat.py <schema.sql> <label> [--fk-on]
Builds a fresh in-memory SQLite DB from schema + seed, runs each test, prints and saves JSON.
Expected values are computed independently in Python, not copied from the SQL under test."""
import sqlite3, sys, json

schema, label = sys.argv[1], sys.argv[2]
fk_on = '--fk-on' in sys.argv
QUERIES = open('queries.sql').read()
Q1 = QUERIES.split('-- Q2')[0].split('\n', 1)[1]
Q2 = QUERIES.split('-- Q2')[1].split('-- Q3')[0].split('\n', 1)[1]
Q3 = QUERIES.split('-- Q3')[1].split('-- Q4')[0].split('\n', 1)[1]


def fresh():
    db = sqlite3.connect(':memory:')
    if fk_on:
        db.execute('PRAGMA foreign_keys = ON')
    db.executescript(open(schema).read())
    db.executescript(open('seed.sql').read())
    return db


def rejected(sql):
    db = fresh()
    try:
        db.execute(sql)
        db.commit()
        return False
    except sqlite3.Error:
        return True


results = []


def case(tid, story, title, expected, fn):
    try:
        ok, actual = fn()
    except Exception as e:
        ok, actual = False, 'error: ' + str(e)
    results.append({'id': tid, 'story': story, 'title': title, 'expected': expected,
                    'actual': actual, 'result': 'PASS' if ok else 'FAIL'})


def reject_case(tid, story, title, sql):
    def run():
        r = rejected(sql)
        return r, 'rejected' if r else 'accepted (should have been rejected)'
    case(tid, story, title, 'Statement rejected', run)


def t01():
    db = fresh()
    db.execute("INSERT INTO orders VALUES (200,1,'2026-10-02','Placed',NULL)")
    db.execute("INSERT INTO order_items VALUES (200,3,5)")
    n = db.execute("SELECT COUNT(*) FROM order_items WHERE order_id=200").fetchone()[0]
    return n == 1, f'{n} line item stored'


case('T01', 'US-01', 'Enter an order with one line item', 'Order and line item stored', t01)
reject_case('T02', 'US-02', 'Reject a line item with quantity 0', "INSERT INTO order_items VALUES (101,4,0)")
reject_case('T03', 'US-02', 'Reject a line item with negative quantity', "INSERT INTO order_items VALUES (101,4,-5)")
reject_case('T04', 'US-03', "Reject an invalid order status ('Lost')", "INSERT INTO orders VALUES (201,1,'2026-10-03','Lost',NULL)")
reject_case('T05', 'US-04', 'Reject a duplicate product code (SKU)', "INSERT INTO products VALUES (99,'CUP-12','Dup','Packaging',1,2,5,1)")
reject_case('T06', 'US-05', 'Reject a line item for a product that does not exist', "INSERT INTO order_items VALUES (101,999,1)")
reject_case('T07', 'US-06', 'Block a pick that exceeds on-hand stock', "UPDATE inventory SET on_hand = on_hand - 500 WHERE product_id=3")


def t08():
    db = fresh()
    before = db.execute("SELECT on_hand FROM inventory WHERE product_id=4").fetchone()[0]
    db.execute("UPDATE inventory SET on_hand = on_hand - 12 WHERE product_id=4")
    after = db.execute("SELECT on_hand FROM inventory WHERE product_id=4").fetchone()[0]
    return after == before - 12, f'{before} -> {after}'


case('T08', 'US-07', 'Picking 12 units reduces stock by 12', 'on_hand falls by 12', t08)


def reorder_expected(db):
    out = []
    for sku, onhand, rp in db.execute("SELECT p.sku, i.on_hand, p.reorder_point FROM products p JOIN inventory i ON i.product_id=p.product_id"):
        if onhand <= rp:
            out.append(sku)
    return sorted(out)


def reorder_actual(db):
    return sorted(r[0] for r in db.execute(Q1).fetchall())


def t09():
    db = fresh()
    e, a = reorder_expected(db), reorder_actual(db)
    return e == a, str(a)


case('T09', 'US-08', 'Reorder list matches an independent calculation', 'Same set of SKUs', t09)


def t10():
    db = fresh()
    db.execute("UPDATE inventory SET on_hand = 15 WHERE product_id=8")  # Steel Tumbler drops to its reorder point
    a = reorder_actual(db)
    return 'TUM-S' in a, 'TUM-S now on the list' if 'TUM-S' in a else 'TUM-S missing from the list'


case('T10', 'US-09', 'A product that falls to its reorder point appears on the list', 'TUM-S appears', t10)


def t11():
    db = fresh()
    py = {}
    for oid, st in db.execute("SELECT order_id,status FROM orders").fetchall():
        if st == 'Cancelled':
            continue
        for pid, qty in db.execute("SELECT product_id,qty FROM order_items WHERE order_id=?", (oid,)).fetchall():
            cat, price = db.execute("SELECT category,unit_price FROM products WHERE product_id=?", (pid,)).fetchone()
            py[cat] = py.get(cat, 0) + qty * price
    got = {c: r for c, r, _ in db.execute(Q2)}
    ok = set(got) == set(py) and all(abs(got[k] - round(v, 2)) < 0.01 for k, v in py.items())
    return ok, str({k: round(v, 2) for k, v in got.items()})


case('T11', 'US-10', 'Revenue by category excludes cancelled orders and matches Python', 'Equal within 1 cent', t11)


def t12():
    db = fresh()
    bad = []
    for cat, rev, m in db.execute(Q2).fetchall():
        tot = cost = 0.0
        rows = db.execute("SELECT o.status, oi.qty, p.unit_price, p.unit_cost FROM order_items oi JOIN orders o ON o.order_id=oi.order_id JOIN products p ON p.product_id=oi.product_id WHERE p.category=?", (cat,)).fetchall()
        for st, qty, price, c in rows:
            if st == 'Cancelled':
                continue
            tot += qty * price
            cost += qty * c
        exp = round(100 * (tot - cost) / tot, 1)
        if abs(exp - m) > .05:
            bad.append((cat, exp, m))
    return not bad, 'margins match' if not bad else str(bad)


case('T12', 'US-10', 'Gross margin percent matches Python', 'Equal to 0.1', t12)


def t13():
    db = fresh()
    got = {r: (n, d) for r, n, d in db.execute(Q3)}
    return got['North'][0] == 3 and got['South'] == (1, 6.0), str(got)


case('T13', 'US-11', 'Days-to-ship counts only shipped or delivered orders', 'North 3 orders; South 1 order at 6.0 days', t13)
reject_case('T14', 'US-12', "Reject a 'Shipped' order that has no ship date", "INSERT INTO orders VALUES (202,2,'2026-10-04','Shipped',NULL)")
reject_case('T15', 'US-01', 'Reject the same product twice on one order', "INSERT INTO order_items VALUES (101,1,5)")

passed = sum(r['result'] == 'PASS' for r in results)
print(f'== {label} (foreign_keys={"ON" if fk_on else "default OFF"}): {passed}/{len(results)} passed')
for r in results:
    line = f"{r['id']} {r['result']:4} {r['story']:6} {r['title']}"
    if r['result'] != 'PASS':
        line += '  -> ' + str(r['actual'])
    print(line)
json.dump({'label': label, 'foreign_keys': 'ON' if fk_on else 'OFF (SQLite default)', 'passed': passed,
           'total': len(results), 'results': results}, open(f'uat_{label}.json', 'w'), indent=1)
