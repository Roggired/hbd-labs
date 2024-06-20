from typing import List, Any, Dict
from airflow.models import Variable


class Payment:
    def __init__(
        self,
        payment_id: int,
        payment_year: int,
        payment_month: int,
        payment_sum: int,
    ):
        self.payment_id = payment_id
        self.payment_year = payment_year
        self.payment_month = payment_month
        self.payment_sum = payment_sum


class Order:
    def __init__(
        self,
        id: str,
        deliveryman_id: str,
        payment_id: int,
        delivery_id: str,
    ):
        self.id = id
        self.deliveryman_id = deliveryman_id
        self.payment_id = payment_id
        self.delivery_id = delivery_id


class Deliveryman:
    def __init__(
        self,
        deliveryman_id: str,
        deliveryman_name: str,
    ):
        self.deliveryman_id = deliveryman_id
        self.deliveryman_name = deliveryman_name


class Delivery:
    def __init__(
        self,
        id: str,
        rating: int,
        tips: int,
    ):
        self.id = id
        self.rating = rating
        self.tips = tips


def process_payment(vals: List[List[Any]]) -> str:
    ids = list(
        map(
            lambda val: str(val[0]),
            vals
        )
    )

    return f"SELECT * FROM dds.dm_orders WHERE payment_id IN ({','.join(ids)})"


def process_data_from_dds(
    payments_raw: List[List],
    orders_raw: List[List],
    deliverymans_raw: List[List],
    deliveries_raw: List[List],
) -> List[str]:
    date_config: dict = Variable.get(
        key='CDM__target_date_config',
        deserialize_json=True,
    )
    year: int = date_config['year']
    month: int = date_config['month']

    payments: List[Payment] = list(
        map(
            lambda row: Payment(
                payment_id=row[0],
                payment_year=row[1],
                payment_month=row[2],
                payment_sum=row[3],
            ),
            payments_raw,
        )
    )

    orders: List[Order] = list(
        map(
            lambda row: Order(
                id=row[0],
                deliveryman_id=row[1],
                payment_id=row[2],
                delivery_id=row[3],
            ),
            orders_raw,
        )
    )

    deliverymans: List[Deliveryman] = list(
        map(
            lambda row: Deliveryman(
                deliveryman_id=row[0],
                deliveryman_name=row[1],
            ),
            deliverymans_raw,
        )
    )

    deliveries: List[Delivery] = list(
        map(
            lambda row: Delivery(
                id=row[0],
                rating=row[1],
                tips=row[2],
            ),
            deliveries_raw,
        )
    )

    orders_map: Dict[str, List[Order]] = {}
    for order in orders:
        if order.deliveryman_id not in orders_map:
            orders_map[order.deliveryman_id] = []
        orders_map[order.deliveryman_id].append(order)

    payments_map: Dict[int, Payment] = {}
    for payment in payments:
        payments_map[payment.payment_id] = payment

    deliveries_map: Dict[str, Delivery] = {}
    for delivery in deliveries:
        deliveries_map[delivery.id] = delivery

    operations: List[str] = []
    for deliveryman in deliverymans:
        orders_amount: int = 0
        orders_total_cost: int = 0
        rating_total: int = 0
        rating_amount: int = 0
        tips: int = 0

        orders: List[Order] = orders_map[deliveryman.deliveryman_id]
        for order in orders:
            orders_amount += 1
            orders_total_cost += payments_map.get(
                order.payment_id,
                Payment(payment_id=0, payment_year=0, payment_month=0, payment_sum=0)
            ).payment_sum
            if order.delivery_id in deliveries_map:
                rating_total += deliveries_map[order.delivery_id].rating
                rating_amount += 1
            tips += deliveries_map.get(
                order.delivery_id,
                Delivery(id='', rating=0, tips=0)
            ).tips

        deliveryman_order_income: float
        rating: float = (rating_total / rating_amount) if rating_amount > 0 else 0

        if rating < 10:
            from_orders_deliveryman_commission: float = orders_total_cost * 0.05
            if from_orders_deliveryman_commission < 400:
                from_orders_deliveryman_commission = 400

            deliveryman_order_income = from_orders_deliveryman_commission
        else:
            from_orders_deliveryman_commission: float = orders_total_cost * 0.1
            if from_orders_deliveryman_commission > 1000:
                from_orders_deliveryman_commission = 1000

            deliveryman_order_income = from_orders_deliveryman_commission

        operations.append(
            f"""
                INSERT INTO cdm.deliveryman_income(
                    deliveryman_id,
                    deliveryman_name,
                    year,
                    month,
                    orders_amount,
                    orders_total_cost,
                    rating,
                    company_commission,
                    deliveryman_order_income,
                    tips
                )
                VALUES (
                    '{deliveryman.deliveryman_id}',
                    '{deliveryman.deliveryman_name}',
                    {year},
                    {month},
                    {orders_amount},
                    {orders_total_cost},
                    {rating},
                    {orders_total_cost * 0.5},
                    {deliveryman_order_income},
                    {tips}
                )
            """
        )

        return operations
