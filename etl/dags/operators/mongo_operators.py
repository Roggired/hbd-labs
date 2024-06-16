import datetime
from typing import Any, Callable, List

from airflow.models.baseoperator import BaseOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.utils.context import Context


class MongoFetchManyOperator(BaseOperator):
    def __init__(self, mongo_conn_id: str, query_provider: Callable[[], dict], mongo_collection: str, task_id: str, **kwargs):
        super().__init__(task_id=task_id, **kwargs)
        self._mongo_conn_id = mongo_conn_id
        self._query_provider = query_provider
        self._mongo_collection = mongo_collection

    def execute(self, context: Context) -> Any:
        mongo_hook = MongoHook(mongo_conn_id=self._mongo_conn_id)

        entries: List[dict] = list(
            mongo_hook.find(
                mongo_collection=self._mongo_collection,
                query=self._query_provider(),
                find_one=False
            )
        )

        for entry in entries:
            entry['_id'] = str(entry['_id'])
            entry['update_time'] = str(datetime.datetime.fromtimestamp(int(entry['update_time']['$date']['$numberLong']) / 1000))

        if self._mongo_collection == 'Restaurant':
            for entry in entries:
                for menu in entry['menu']:
                    menu['_id'] = str(menu['_id'])

        if self._mongo_collection == 'Orders':
            for entry in entries:
                entry['restaurant']['id'] = str(entry['restaurant']['id'])
                entry['client']['id'] = str(entry['client']['id'])
                entry['order_date'] = str(datetime.datetime.fromtimestamp(int(entry['order_date']['$date']['$numberLong']) / 1000))
                for ordered_dish in entry['ordered_dish']:
                    ordered_dish['id'] = str(ordered_dish['id'])

        return entries
