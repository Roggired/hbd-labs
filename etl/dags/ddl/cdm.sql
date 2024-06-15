CREATE SCHEMA IF NOT EXISTS cdm AUTHORIZATION CURRENT_USER;

CREATE TABLE IF NOT EXISTS cdm.deliveryman_income
(
    id                       BIGSERIAL PRIMARY KEY,
    deliveryman_id           BIGINT           NOT NULL,
    deliveryman_name         VARCHAR(255)     NOT NULL,
    year                     INT              NOT NULL,
    month                    INT              NOT NULL,
    orders_amount            INT              NOT NULL,
    orders_total_cost        DOUBLE PRECISION NOT NULL,
    rating                   DOUBLE PRECISION NOT NULL,
    company_commission       DOUBLE PRECISION NOT NULL,
    deliveryman_order_income DOUBLE PRECISION NOT NULL,
    tips                     DOUBLE PRECISION NOT NULL
);
