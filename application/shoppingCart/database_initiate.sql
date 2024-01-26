INSERT INTO Product (name, price) VALUES ('12 rules for life', '12');
INSERT INTO Product (name, price) VALUES ('twilight', '10');
INSERT INTO Product (name, price) VALUES ('atomic habits', '15');
INSERT INTO Product (name, price) VALUES ('5am club', '20');


INSERT INTO Cart (total, user_id, exp_date) VALUES (0.0, null, '2024-02-15');
INSERT INTO Cart (total, user_id, exp_date) VALUES (0.0, null, '2024-02-15');
INSERT INTO Cart (total, user_id, exp_date) VALUES (0.0, null, '2024-02-15');

INSERT INTO Cart_Item (cart_id, product_id, name, quantity, price)
VALUES
    (1, 1, '12 rules for life', 1, 12.0),
    (1, 2, 'twilight', 2, 10.0),
    (2, 1, '12 rules for life', 1, 12.0),
    (2, 3, 'atomic habits', 1, 15.0),
    (3, 3, 'atomic habits', 2, 15.0),
    (3, 4, '5am club', 1, 20.0);

UPDATE cart SET total = 32.0 where cart_id = 1;
UPDATE cart SET total = 27.0 where cart_id = 2;
UPDATE cart SET total = 50.0 where cart_id = 3;