create table orders
(
    id                 uuid primary key,
    order_date_created timestamp        not null,
    delivery_id        varchar(255)     not null,
    deliveryman_id     varchar(255)     not null,
    delivery_address   text             not null,
    delivery_time      timestamp        not null,
    rating             double precision not null,
    tips               double precision
);