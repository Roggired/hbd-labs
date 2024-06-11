CREATE SCHEMA staging AUTHORIZATION CURRENT_USER ;

CREATE TABLE staging.pg_dish(
    dish_id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    price BIGINT,
    when_created TIMESTAMP,
    when_updated TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE staging.pg_category
(
    category_id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    percent INT,
    min_payment INT,
    when_created TIMESTAMP,
    when_updated TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE staging.pg_client
(
    client_id BIGINT PRIMARY KEY,
    bonus_balance BIGINT,
    category_id BIGINT,
    when_created TIMESTAMP,
    when_updated TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE staging.pg_payment
(
    payment_id BIGINT PRIMARY KEY,
    client_id BIGINT,
    dish_id BIGINT,
    dish_amount INT,
    order_id VARCHAR(255),
    order_time TIMESTAMP,
    order_sum BIGINT,
    tips BIGINT,
    when_created TIMESTAMP,
    when_updated TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE staging.mongo_clients
(

);
