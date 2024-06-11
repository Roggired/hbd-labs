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
    id            VARCHAR(31) PRIMARY KEY,
    name          VARCHAR(255),
    phone         VARCHAR(255),
    birthday      DATE,
    email         VARCHAR(255),
    login         VARCHAR(255),
    address       VARCHAR(511),
    update_time   TIMESTAMP,
    when_created  TIMESTAMP,
    when_updated  TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE staging.mongo_orders
(
    id               VARCHAR(31) PRIMARY KEY,
    restaurant       VARCHAR(31),
    order_date       TIMESTAMP,
    client           VARCHAR(31),
    payed_by_bonuses DOUBLE PRECISION,
    cost             DOUBLE PRECISION,
    payment          DOUBLE PRECISION,
    bonus_for_visit  DOUBLE PRECISION,
    final_status     VARCHAR(31),
    update_time      time_stamp,
    when_created     TIMESTAMP,
    when_updated     TIMESTAMP,
    when_uploaded    TIMESTAMP
);

CREATE TABLE staging.mongo_ordered_dish
(
    id             VARCHAR(31) PRIMARY KEY,
    name           VARCHAR(255),
    price          DOUBLE PRECISION,
    quantity       SMALLINT,
    mongo_order_id VARCHAR(31) REFERENCES staging.mongo_orders (id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE staging.mongo_order_statuses
(
    id             VARCHAR(31) PRIMARY KEY,
    status         VARCHAR(31),
    time           TIMESTAMP,
    mongo_order_id VARCHAR(31) REFERENCES staging.mongo_orders (id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE staging.mongo_restaurant
(
    id            VARCHAR(31) PRIMARY KEY,
    name          VARCHAR(255),
    phone         VARCHAR(255),
    email         VARCHAR(255),
    founding_day  DATE,
    update_time   TIMESTAMP,
    when_created  TIMESTAMP,
    when_updated  TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE staging.mongo_restaurant_menu
(
    id                  VARCHAR(31) PRIMARY KEY,
    name                VARCHAR(255),
    price               DOUBLE PRECISION,
    dish_category       VARCHAR(255),
    mongo_restaurant_id VARCHAR(31) REFERENCES staging.mongo_restaurant ON DELETE CASCADE NOT NULL
);

CREATE TABLE staging.api_deliveryman
(
    id VARCHAR(31) PRIMARY KEY ,
    name VARCHAR(255),
    when_created TIMESTAMP,
    when_updated TIMESTAMP,
    when_uploaded TIMESTAMP
);

CREATE TABLE staging.api_delivery
(
    delivery_id VARCHAR(31) PRIMARY KEY,
    deliveryman_id VARCHAR(31),
    delivery_address VARCHAR(255),
    delivery_time TIMESTAMP,
    order_id VARCHAR(31),
    order_date_created TIMESTAMP,
    rating SMALLINT,
    tips DOUBLE PRECISION,
    when_created TIMESTAMP,
    when_updated TIMESTAMP,
    when_uploaded TIMESTAMP
);
