INSERT INTO suppliers VALUES (1,'Northside Supply',3),(2,'Lakeview Wholesale',7),(3,'Prairie Goods',5);
INSERT INTO products VALUES
 (1,'CUP-12','Paper Cup 12oz','Packaging',0.10,0.25,500,1),(2,'LID-12','Cup Lid 12oz','Packaging',0.05,0.15,500,1),
 (3,'BEAN-1','Coffee Beans 1lb','Beverage',6.00,12.00,40,2),(4,'SYR-V','Vanilla Syrup','Beverage',3.50,7.50,25,2),
 (5,'NAP-100','Napkins 100ct','Supplies',1.20,2.99,60,3),(6,'STR-50','Straws 50ct','Supplies',0.90,2.49,60,3),
 (7,'MUG-C','Ceramic Mug','Merchandise',4.00,11.99,20,3),(8,'TUM-S','Steel Tumbler','Merchandise',9.00,24.99,15,2);
INSERT INTO inventory VALUES (1,420),(2,900),(3,35),(4,60),(5,25),(6,140),(7,12),(8,30);
INSERT INTO customers VALUES (1,'Maple Cafe','North'),(2,'Oak Office Park','West'),(3,'Birch Catering','North'),(4,'Cedar Events','South'),(5,'Elm Bakery','West');
INSERT INTO orders VALUES
 (101,1,'2026-09-01','Delivered','2026-09-02'),(102,2,'2026-09-03','Delivered','2026-09-07'),(103,3,'2026-09-05','Delivered','2026-09-06'),
 (104,1,'2026-09-12','Delivered','2026-09-13'),(105,4,'2026-09-15','Delivered','2026-09-21'),(106,5,'2026-09-18','Shipped','2026-09-20'),
 (107,2,'2026-09-22','Placed',NULL),(108,3,'2026-09-25','Cancelled',NULL),(109,1,'2026-09-28','Picked',NULL),(110,4,'2026-10-01','Placed',NULL);
INSERT INTO order_items VALUES
 (101,1,300),(101,2,300),(101,3,10),(102,5,40),(102,6,40),(102,7,6),(103,3,20),(103,4,10),(104,1,200),(104,3,8),
 (105,8,10),(105,7,8),(106,5,30),(106,6,30),(107,3,15),(107,4,6),(108,1,100),(109,3,12),(109,2,150),(110,7,10),(110,8,5);
