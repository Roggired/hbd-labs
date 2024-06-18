import datetime
import pytz


class APIProcessor:
    def __init__(self):
        self._delivery_time = datetime.datetime(1900, 1, 1, tzinfo=pytz.utc)

    def process_delivery(
        self,
        entity: dict,
    ) -> str:
        delivery_time = datetime.datetime.fromisoformat(entity['delivery_time'])
        if delivery_time > self._delivery_time:
            self._delivery_time = delivery_time
        return f"""
            INSERT INTO staging.api_delivery
            VALUES (
                '{entity['delivery_id']}',
                '{entity['deliveryman_id']}',
                '{entity['delivery_address']}',
                '{entity['delivery_time']}',
                '{entity['order_id']}',
                '{entity['order_date_created']}',
                {entity['rating']},
                {entity['tips']},
                null,
                null,
                '{datetime.datetime.now(tz=pytz.utc).isoformat()}'
            )
        """

    def process_deliveryman(
        self,
        entity: dict,
    ) -> str:
        return f"""
            INSERT INTO staging.api_deliveryman
            VALUES (
                '{entity['id']}',
                '{entity['name']}',
                null,
                null,
                '{datetime.datetime.now(tz=pytz.utc).isoformat()}'
            )
        """

    def get_last_delivery_time(self):
        return self._delivery_time
