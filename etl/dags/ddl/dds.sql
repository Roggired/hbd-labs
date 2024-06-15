CREATE SCHEMA IF NOT EXISTS dds AUTHORIZATION CURRENT_USER;

CREATE TABLE IF NOT EXISTS dds.dm_deliveryman
(
    deliveryman_id BIGINT PRIMARY KEY,
    name           VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS dds.dm_payments
(
    payment_id    BIGINT PRIMARY KEY,
    payment_year  INT NOT NULL,
    payment_month INT NOT NULL
);

CREATE TABLE IF NOT EXISTS dds.dm_deliveries
(
    id                BIGINT PRIMARY KEY,
    orders_amount     INT              NOT NULL,
    orders_total_cost DOUBLE PRECISION NOT NULL,
    rating            SMALLINT         NOT NULL,
    tips              SMALLINT         NOT NULL
);

-- Снежинка
CREATE TABLE IF NOT EXISTS dds.dm_orders
(
    id            BIGINT PRIMARY KEY,
    client_id     BIGINT REFERENCES dds.dm_deliveryman (deliveryman_id) ON DELETE CASCADE NOT NULL,
    restaurant_id BIGINT REFERENCES dds.dm_payments (payment_id) ON DELETE CASCADE        NOT NULL,
    delivery_id   BIGINT REFERENCES dds.dm_deliveries (id) ON DELETE CASCADE              NOT NULL
);

-- CREATE TABLE IF NOT EXISTS staging.mongo_clients
-- (
--     id            VARCHAR(31) PRIMARY KEY,
--     name          VARCHAR(255),
--     phone         VARCHAR(255),
--     birthday      DATE,
--     email         VARCHAR(255),
--     login         VARCHAR(255),
--     address       VARCHAR(511),
--     update_time   TIMESTAMP,
--     when_created  TIMESTAMP,
--     when_updated  TIMESTAMP,
--     when_uploaded TIMESTAMP
-- );
--
-- CREATE TABLE IF NOT EXISTS staging.mongo_orders
-- (
--     id               VARCHAR(31) PRIMARY KEY,
--     restaurant       VARCHAR(31),
--     order_date       TIMESTAMP,
--     client           VARCHAR(31),
--     payed_by_bonuses DOUBLE PRECISION,
--     cost             DOUBLE PRECISION,
--     payment          DOUBLE PRECISION,
--     bonus_for_visit  DOUBLE PRECISION,
--     final_status     VARCHAR(31),
--     update_time      time_stamp,
--     when_created     TIMESTAMP,
--     when_updated     TIMESTAMP,
--     when_uploaded    TIMESTAMP
-- );
--
-- CREATE TABLE IF NOT EXISTS staging.mongo_ordered_dish
-- (
--     id             VARCHAR(31) PRIMARY KEY,
--     name           VARCHAR(255),
--     price          DOUBLE PRECISION,
--     quantity       SMALLINT,
--     mongo_order_id VARCHAR(31) REFERENCES staging.mongo_orders (id) ON DELETE CASCADE NOT NULL
-- );
--
-- CREATE TABLE IF NOT EXISTS staging.mongo_order_statuses
-- (
--     id             VARCHAR(31) PRIMARY KEY,
--     status         VARCHAR(31),
--     time           TIMESTAMP,
--     mongo_order_id VARCHAR(31) REFERENCES staging.mongo_orders (id) ON DELETE CASCADE NOT NULL
-- );
--
-- CREATE TABLE IF NOT EXISTS staging.mongo_restaurant
-- (
--     id            VARCHAR(31) PRIMARY KEY,
--     name          VARCHAR(255),
--     phone         VARCHAR(255),
--     email         VARCHAR(255),
--     founding_day  DATE,
--     update_time   TIMESTAMP,
--     when_created  TIMESTAMP,
--     when_updated  TIMESTAMP,
--     when_uploaded TIMESTAMP
-- );
--
-- CREATE TABLE IF NOT EXISTS staging.mongo_restaurant_menu
-- (
--     id                  VARCHAR(31) PRIMARY KEY,
--     name                VARCHAR(255),
--     price               DOUBLE PRECISION,
--     dish_category       VARCHAR(255),
--     mongo_restaurant_id VARCHAR(31) REFERENCES staging.mongo_restaurant ON DELETE CASCADE NOT NULL
-- );
