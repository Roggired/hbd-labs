from datetime import datetime
from typing import Any, List


class Log:
    def __init__(
        self,
        _id: int,
        entity_id: int,
        table_name: str,
        time: datetime,
        values: dict,
        action: str,
    ):
        self.id = _id
        self.entity_id = entity_id
        self.table_name = table_name
        self.time = time
        self.values = values
        self.action = action
        self.parsed_values: dict = values


class PostgresProcessor:
    def __init__(self, last_loaded_log_id: int):
        self._last_processed_log_id: int = last_loaded_log_id

    def process_log_row_into_operation(
        self,
        row: List[Any],
    ) -> str:
        log: Log = self._parse_log_entity(row)

        if log.table_name == 'dish':
            return self._process_dish_changes(log)
        elif log.table_name == 'category':
            return self._process_category_changes(log)
        elif log.table_name == 'client':
            return self._process_client_changes(log)
        elif log.table_name == 'payment':
            return self._process_payment_changes(log)
        else:
            raise RuntimeError(f"Unexpected table_name: {log.table_name}")

    def _parse_log_entity(
        self,
        row: List[Any],
    ) -> Log:
        self._last_processed_log_id = row[0]
        return Log(
            _id=row[0],
            entity_id=row[1],
            table_name=row[2],
            time=row[3],
            values=row[4],
            action=row[5],
        )

    def _process_dish_changes(self, log: Log) -> str:
        if log.action == 'INSERT':
            return f"""
                INSERT INTO staging.pg_dish(dish_id, name, price, when_created, when_updated, when_uploaded)
                VALUES ({log.parsed_values['dish_id']},'{log.parsed_values['name']}',{log.parsed_values['price']},'{str(log.time)}','{str(log.time)}','{str(datetime.now())}')
            """
        elif log.action == 'UPDATE':
            return f"""
                UPDATE staging.pg_dish
                SET name='{log.parsed_values['name']}', price={log.parsed_values['price']}, when_updated='{str(log.time)}', when_uploaded='{str(datetime.now())}'
                WHERE dish_id={log.parsed_values['dish_id']}
            """
        else:
            return f"""
                DELETE FROM staging.pg_dish
                WHERE dish_id={log.parsed_values['dish_id']}
            """

    def _process_category_changes(self, log: Log) -> str:
        if log.action == 'INSERT':
            return f"""
                INSERT INTO staging.pg_category(category_id, name, percent, min_payment, when_created, when_updated, when_uploaded)
                VALUES ({log.parsed_values['category_id']},'{log.parsed_values['name']}',{log.parsed_values['percent']},{log.parsed_values['min_payment']},'{str(log.time)}','{str(log.time)}','{str(datetime.now())}')
            """
        elif log.action == 'UPDATE':
            return f"""
                UPDATE staging.pg_category
                SET name='{log.parsed_values['name']}', percent={log.parsed_values['percent']}, min_payment={log.parsed_values['min_payment']}, when_updated='{str(log.time)}', when_uploaded='{str(datetime.now())}'
                WHERE category_id={log.parsed_values['category_id']}
            """
        else:
            return f"""
                DELETE FROM staging.pg_category
                WHERE category_id={log.parsed_values['category_id']}
            """

    def _process_client_changes(self, log: Log) -> str:
        if log.action == 'INSERT':
            return f"""
                INSERT INTO staging.pg_client(client_id, bonus_balance, category_id, when_created, when_updated, when_uploaded)
                VALUES ({log.parsed_values['client_id']},{log.parsed_values['bonus_balance']},{log.parsed_values['category_id']},'{str(log.time)}','{str(log.time)}','{str(datetime.now())}')
            """
        elif log.action == 'UPDATE':
            return f"""
                UPDATE staging.pg_client
                SET bonus_balance={log.parsed_values['bonus_balance']}, category_id={log.parsed_values['category_id']}, when_updated='{str(log.time)}', when_uploaded='{str(datetime.now())}'
                WHERE client_id={log.parsed_values['client_id']}
            """
        else:
            return f"""
                DELETE FROM staging.pg_client
                WHERE client_id={log.parsed_values['client_id']}
            """

    def _process_payment_changes(self, log: Log) -> str:
        if log.action == 'INSERT':
            return f"""
                INSERT INTO staging.pg_payment(
                    payment_id, 
                    client_id, 
                    dish_id, 
                    dish_amount, 
                    order_id, 
                    order_time, 
                    order_sum, 
                    tips, 
                    when_created, 
                    when_updated, 
                    when_uploaded
                )
                VALUES (
                    {log.parsed_values['payment_id']},
                    {log.parsed_values['client_id']},
                    {log.parsed_values['dish_id']},
                    {log.parsed_values['dish_amount']},
                    '{log.parsed_values['order_id']}',
                    '{log.parsed_values['order_time']}',
                    {log.parsed_values['order_sum']},
                    {log.parsed_values['tips']},
                    '{str(log.time)}',
                    '{str(log.time)}',
                    '{str(datetime.now())}'
                )
            """
        elif log.action == 'UPDATE':
            return f"""
                UPDATE staging.pg_payment
                SET 
                    client_id={log.parsed_values['client_id']}, 
                    dish_id={log.parsed_values['dish_id']}, 
                    dish_amount={log.parsed_values['dish_amount']}, 
                    order_id='{log.parsed_values['order_id']}', 
                    order_time='{log.parsed_values['order_time']}', 
                    order_sum={log.parsed_values['order_sum']}, 
                    tips={log.parsed_values['tips']}, 
                    when_updated='{str(log.time)}', 
                    when_uploaded='{str(datetime.now())}'
                WHERE payment_id={log.parsed_values['payment_id']}
            """
        else:
            return f"""
                DELETE FROM staging.pg_payment
                WHERE payment_id={log.parsed_values['payment_id']}
            """

    def get_last_processed_log_id(self) -> int:
        return self._last_processed_log_id
