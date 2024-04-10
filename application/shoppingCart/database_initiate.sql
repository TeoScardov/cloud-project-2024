INSERT INTO Product ("id","name", "price") VALUES ('94ff3b8b-56bf-453d-af20-a2fd78feae55','12 rules for life', '12');
INSERT INTO Product ("id","name", "price") VALUES ('df201f5e-4c4d-4fca-9510-946254901300','twilight', '10');
INSERT INTO Product ("id","name", "price") VALUES ('50bc44b0-adc6-4b93-9df0-f5a96df580b3','atomic habits', '15');
INSERT INTO Product ("id","name", "price") VALUES ('f5285e4b-85c2-42ae-b2f4-848f676f04cc','5am club', '20');


INSERT INTO Cart ("id",total, user_id, exp_date) VALUES ('6c6f4cc2-c0f5-4010-9389-7e2887351eb2',0.0, null, '2024-02-15');
INSERT INTO Cart ("id",total, user_id, exp_date) VALUES ('f36a37b6-1cc2-425e-a9f4-e978c8376abb',0.0, null, '2024-02-15');
INSERT INTO Cart ("id",total, user_id, exp_date) VALUES ('71ce137f-21cf-40ed-8de9-3b845d42c28c',0.0, null, '2024-02-15');

INSERT INTO Cart_Item (cart_id, product_id, name, quantity, price)
VALUES
    ('6c6f4cc2-c0f5-4010-9389-7e2887351eb2', '94ff3b8b-56bf-453d-af20-a2fd78feae55', '12 rules for life', 1, 12.0),
    ('6c6f4cc2-c0f5-4010-9389-7e2887351eb2', 'df201f5e-4c4d-4fca-9510-946254901300', 'twilight', 2, 10.0),
    ('f36a37b6-1cc2-425e-a9f4-e978c8376abb', '94ff3b8b-56bf-453d-af20-a2fd78feae55', '12 rules for life', 1, 12.0),
    ('f36a37b6-1cc2-425e-a9f4-e978c8376abb', '50bc44b0-adc6-4b93-9df0-f5a96df580b3', 'atomic habits', 1, 15.0),
    ('71ce137f-21cf-40ed-8de9-3b845d42c28c', '50bc44b0-adc6-4b93-9df0-f5a96df580b3', 'atomic habits', 2, 15.0),
    ('71ce137f-21cf-40ed-8de9-3b845d42c28c', 'f5285e4b-85c2-42ae-b2f4-848f676f04cc', '5am club', 1, 20.0);

UPDATE cart SET total = 32.0 where id = '6c6f4cc2-c0f5-4010-9389-7e2887351eb2';
UPDATE cart SET total = 27.0 where id = 'f36a37b6-1cc2-425e-a9f4-e978c8376abb';
UPDATE cart SET total = 50.0 where id = '71ce137f-21cf-40ed-8de9-3b845d42c28c';