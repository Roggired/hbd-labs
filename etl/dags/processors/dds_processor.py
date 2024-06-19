import datetime
from typing import List, Any


def process_payment(vals: List[Any]) -> str:
    order_time: datetime.datetime = vals[5]
    return f"INSERT INTO dds.dm_payments (payment_id, payment_year, payment_month, payment_sum) VALUES ({vals[0]}, {order_time.year}, {order_time.month}, {vals[6]})"


def process_delivery(vals: List[Any]) -> str:
    return f"INSERT INTO dds.dm_deliveries (id, rating, tips) VALUES ('{vals[0]}', {vals[6]}, {vals[7]})"


def process_deliveryman(vals: List[Any]) -> str:
    return f"INSERT INTO dds.dm_deliveryman (deliveryman_id, deliveryman_name) VALUES ('{vals[0]}', '{vals[1]}')"


def process_order(order: List[Any], payment: List[Any], delivery: List[Any], deliveryman: List[Any]) -> str:
    order_id = order[1]
    payment_id = payment[0]
    delivery_id = delivery[0]
    deliveryman_id = deliveryman[0]
    return f"INSERT INTO dds.dm_orders (id, deliveryman_id, payment_id, delivery_id) VALUES ('{order_id}', '{deliveryman_id}', {payment_id}, '{delivery_id}')"