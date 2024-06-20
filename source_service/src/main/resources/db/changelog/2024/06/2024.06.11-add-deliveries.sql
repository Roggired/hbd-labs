create table deliveries
(
    delivery_id    VARCHAR(63) primary key,
    order_date_created timestamp        not null,
    order_id       varchar(63)                                                not null,
    deliveryman_id varchar(63) REFERENCES delivery_man (id) ON DELETE CASCADE NOT NULL,
    delivery_address   text             not null,
    delivery_time      timestamp        not null,
    rating             double precision not null,
    tips               double precision
);
