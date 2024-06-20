CREATE SCHEMA IF NOT EXISTS dds AUTHORIZATION CURRENT_USER;

CREATE TABLE IF NOT EXISTS dds.dm_deliveryman
(
    deliveryman_id VARCHAR(63) PRIMARY KEY,
    deliveryman_name           VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS dds.dm_payments
(
    payment_id    BIGINT PRIMARY KEY,
    payment_year  INT NOT NULL,
    payment_month INT NOT NULL,
    payment_sum   BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS dds.dm_deliveries
(
    id                VARCHAR(63) PRIMARY KEY,
    rating            SMALLINT         NOT NULL,
    tips              SMALLINT         NOT NULL
);

-- Снежинка
CREATE TABLE IF NOT EXISTS dds.dm_orders
(
    id              VARCHAR(63) PRIMARY KEY,
    deliveryman_id  VARCHAR(63) REFERENCES dds.dm_deliveryman (deliveryman_id) ON DELETE CASCADE NOT NULL,
    payment_id      BIGINT REFERENCES dds.dm_payments (payment_id) ON DELETE CASCADE        NOT NULL,
    delivery_id     VARCHAR(63) REFERENCES dds.dm_deliveries (id) ON DELETE CASCADE              NOT NULL
);