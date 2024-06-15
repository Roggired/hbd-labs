CREATE SCHEMA IF NOT EXISTS staging AUTHORIZATION CURRENT_USER;

CREATE TABLE IF NOT EXISTS staging.pg_dish
(
    dish_id       BIGINT PRIMARY KEY,
    name          VARCHAR(255),
    price         BIGINT,
    when_created  TIMESTAMP,
    when_updated  TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.pg_category
(
    category_id   BIGINT PRIMARY KEY,
    name          VARCHAR(255),
    percent       INT,
    min_payment   INT,
    when_created  TIMESTAMP,
    when_updated  TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.pg_client
(
    client_id     BIGINT PRIMARY KEY,
    bonus_balance BIGINT,
    category_id   BIGINT,
    when_created  TIMESTAMP,
    when_updated  TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.pg_payment
(
    payment_id    BIGINT PRIMARY KEY,
    client_id     BIGINT,
    dish_id       BIGINT,
    dish_amount   INT,
    order_id      VARCHAR(255),
    order_time    TIMESTAMP,
    order_sum     BIGINT,
    tips          BIGINT,
    when_created  TIMESTAMP,
    when_updated  TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.mongo_clients
(
    id            BIGSERIAL PRIMARY KEY,
    obj_id        VARCHAR(31) NOT NULL UNIQUE,
    obj_val       JSONB       NOT NULL,
    when_created  TIMESTAMP,
    when_updated  TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.mongo_orders
(
    id            BIGSERIAL PRIMARY KEY,
    obj_id        VARCHAR(31) NOT NULL UNIQUE,
    when_created  TIMESTAMP,
    when_updated  TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.mongo_restaurant
(
    id            BIGSERIAL PRIMARY KEY,
    obj_id        VARCHAR(31) NOT NULL UNIQUE,
    when_created  TIMESTAMP,
    when_updated  TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.api_deliveryman
(
    id            VARCHAR(31) PRIMARY KEY,
    name          VARCHAR(255),
    when_created  TIMESTAMP,
    when_updated  TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.api_delivery
(
    delivery_id        VARCHAR(31) PRIMARY KEY,
    deliveryman_id     VARCHAR(31),
    delivery_address   VARCHAR(255),
    delivery_time      TIMESTAMP,
    order_id           VARCHAR(31),
    order_date_created TIMESTAMP,
    rating             SMALLINT,
    tips               DOUBLE PRECISION,
    when_created       TIMESTAMP,
    when_updated       TIMESTAMP,
    when_uploaded      TIMESTAMP
);
