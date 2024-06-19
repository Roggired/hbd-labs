from typing import Any, Dict, Optional, Callable, List

from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
import datetime
import enum
from airflow.models import Variable


class APIFetchOperator(BaseOperator):
    """
        Connection variable format:
        {
            "method": "GET",
            "url": "https://example.com/api/v1/deliveries",
            "entity_type": "DELIVERY"
        }
    """
    def __init__(
        self,
        conn_variable_id: str,
        task_id: str,
        query_params: Optional[Dict[str, Any]] = None,
        body_provider: Optional[Callable[[], Optional[Dict[str, Any]]]] = None,
        **kwargs
    ):
        super().__init__(task_id=task_id, **kwargs)
        self._conn_variable_id = conn_variable_id
        self._query_params = query_params
        self._body_provider = body_provider

    def execute(self, context: Context) -> Any:
        return StubRestHook(self._conn_variable_id).execute(
            query_params=self._query_params,
            body=self._body_provider(),
        )


class APIEntityType(enum.Enum):
    DELIVERY = 0
    DELIVERYMAN = 1


class AbstractRestHook:
    def __init__(self, conn_var_id: str):
        connection: Dict[str, str] = Variable.get(key=conn_var_id, deserialize_json=True)
        url: Optional[str] = connection.get("url", None)
        entity_type: Optional[str] = connection.get("entity_type", None)
        method: str = connection.get("method", "GET")

        if url is None or entity_type is None:
            raise RuntimeError("Connection variable format is invalid")

        self._url: str = url
        self._entity_type: str = entity_type
        self._method: str = method

    def execute(
        self,
        query_params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None
    ) -> dict:
        raise NotImplementedError()


class RealRestHook(AbstractRestHook):
    def __init__(self, conn_var_id: str):
        super().__init__(conn_var_id)

    def execute(
        self,
        query_params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None
    ) -> dict:
        raise NotImplementedError()


class StubRestHook(AbstractRestHook):
    def __init__(self, conn_var_id: str):
        super().__init__(conn_var_id)

    def execute(
        self,
        query_params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None
    ) -> dict:
        if self._entity_type == APIEntityType.DELIVERY.name:
            delivery_time_filter_clause_raw: Optional[str] = None
            if body is not None:
                delivery_time_filter_clause_raw = body.get("delivery_time_filter_clause", None)

            page_number: int = 0
            if query_params is not None:
                page_number = query_params.get("page_number", 0)

                if page_number < 0:
                    raise RuntimeError("Invalid page number")

            page_size: int = 10
            if query_params is not None:
                page_size = query_params.get("page_size", 10)

                if page_size <= 0:
                    raise RuntimeError("Invalid page size")

            delivery_time_filter_clause: Optional[datetime.datetime] = None
            if delivery_time_filter_clause_raw is not None:
                delivery_time_filter_clause = datetime.datetime.fromisoformat(delivery_time_filter_clause_raw)

            filtered_deliveries: List[dict] = list(
                filter(
                    lambda el: datetime.datetime.fromisoformat(el["delivery_time"]) > delivery_time_filter_clause,
                    _TEST_DELIVERIES,
                )
            ) if delivery_time_filter_clause is not None else _TEST_DELIVERIES

            first_index: int = page_number * page_size
            last_index: int = first_index + page_size

            page_content: List[dict] = filtered_deliveries[first_index:last_index]
            return {
                'total_elements': len(filtered_deliveries),
                'total_pages': (
                    len(filtered_deliveries) // page_size
                ) if len(filtered_deliveries) % page_size == 0 else (
                    len(filtered_deliveries) // page_size + 1
                ),
                'content': page_content
            }

        if self._entity_type == APIEntityType.DELIVERYMAN.name:
            number_of_deliverymans_to_skip: int = 0
            if body is not None:
                number_of_deliverymans_to_skip = body.get("number_of_deliverymans_to_skip", 0)

            page_number: int = 0
            if query_params is not None:
                page_number = query_params.get("page_number", 0)

                if page_number < 0:
                    raise RuntimeError("Invalid page number")

            page_size: int = 10
            if query_params is not None:
                page_size = query_params.get("page_size", 10)

                if page_size <= 0:
                    raise RuntimeError("Invalid page size")

            filtered_deliverymans: List[dict] = _TEST_DELIVERYMANS[number_of_deliverymans_to_skip:]

            first_index: int = page_number * page_size
            last_index: int = first_index + page_size

            page_content: List[dict] = filtered_deliverymans[first_index:last_index]
            return {
                'total_elements': len(filtered_deliverymans),
                'total_pages': (
                        len(filtered_deliverymans) // page_size
                ) if len(filtered_deliverymans) % page_size == 0 else (
                        len(filtered_deliverymans) // page_size + 1
                ),
                'content': page_content
            }

        raise RuntimeError("Invalid entity_type supplied")


_TEST_DELIVERIES = [
    {
        "order_id": "6222053d10v01cqw379td1k9",
        "order_date_created": "2024-12-04 12:50:27.43000",
        "delivery_id": "6222053d10v01cqw379td2t8",
        "deliveryman_id": "68ga56cqwcxm79920ft8lkjhg",
        "delivery_address": "Ул. Мира, 7, корпус 1, кв. 4",
        "delivery_time": "2024-12-04 13:11:23.621000+00:00",
        "rating": 5,
        "tips": 500
    },
    {
        "order_id": "772738ba5b1241c78abc7e17",
        "order_date_created": "2024-12-04 12:50:27.43000",
        "delivery_id": "3222053d10v01cqw379td2t8",
        "deliveryman_id": "00ga56cqwcxm789920ft8siqr",
        "delivery_address": "Ул. Мира, 7, корпус 1, кв. 4",
        "delivery_time": "2024-12-04 13:11:23.621000+00:00",
        "rating": 5,
        "tips": 500
    }
]

_TEST_DELIVERYMANS = [
    {"id": "00ga56cqwcxm789920ft8siqr ", "name": "Екатерина Великая"},
    {"id": "68ga56cqwcxm79920ft8lkjhg", "name": "Дора Величковская"}
]
