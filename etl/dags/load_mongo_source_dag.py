import datetime
import pytz
from typing import Any, List, Dict

from airflow.decorators import dag
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.models.taskinstance import TaskInstance
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from operators.mongo_operators import MongoFetchManyOperator
from processors.mongo_processor import MongoCollections


@dag(
    dag_id="load_mongo_source",
    schedule_interval='*/3 * * * *',
    start_date=datetime.datetime(2024, 6, 16),
    catchup=False,
    tags=['load'],
    is_paused_upon_creation=False,
)
def load_mongo_source_dag():
    # --------------------------------------- settings -----------------------------------
    load_settings = SQLExecuteQueryOperator(
        task_id='load_settings',
        conn_id='postgres_dwh',
        sql="SELECT settings FROM staging.settings WHERE source_id = 'MONGO';"
    )

    def process_settings(task_instance: TaskInstance):
        values: List[List[Any]] = task_instance.xcom_pull(task_ids='load_settings')
        settings: Dict[str, Any]
        if len(values) <= 0:
            settings = {
                'last_loaded_timestamp_restaurants': datetime.datetime(1900, 1, 1, tzinfo=pytz.utc),
                'last_loaded_timestamp_orders': datetime.datetime(1900, 1, 1, tzinfo=pytz.utc),
                'last_loaded_timestamp_clients': datetime.datetime(1900, 1, 1, tzinfo=pytz.utc)
            }
            Variable.set(
                key='MONGO__settings_initialized',
                value=False,
                serialize_json=True
            )
        else:
            settings_raw = values[0][0]
            settings = {
                'last_loaded_timestamp_restaurants': datetime.datetime.fromisoformat(settings_raw['last_loaded_timestamp_restaurants']),
                'last_loaded_timestamp_orders': datetime.datetime.fromisoformat(settings_raw['last_loaded_timestamp_orders']),
                'last_loaded_timestamp_clients': datetime.datetime.fromisoformat(settings_raw['last_loaded_timestamp_clients'])
            }
            Variable.set(
                key='MONGO__settings_initialized',
                value=True,
                serialize_json=True
            )

        Variable.set(
            key='MONGO__last_loaded_timestamp_restaurants',
            value=settings['last_loaded_timestamp_restaurants'].isoformat(),
            serialize_json=True
        )
        Variable.set(
            key='MONGO__last_loaded_timestamp_orders',
            value=settings['last_loaded_timestamp_orders'].isoformat(),
            serialize_json=True
        )
        Variable.set(
            key='MONGO__last_loaded_timestamp_clients',
            value=settings['last_loaded_timestamp_clients'].isoformat(),
            serialize_json=True
        )
        return settings
    process_settings_op = PythonOperator(task_id='process_settings', python_callable=process_settings)
    # ------------------------------------------------------------------------------------

    # --------------------------------------- loads restaurants --------------------------
    def query_provider_restaurants() -> dict:
        return {
            "update_time": {
                "$gt": {
                    "$date": {
                        "$numberLong": f'{int(datetime.datetime.fromisoformat(Variable.get('MONGO__last_loaded_timestamp_restaurants', deserialize_json=True)).timestamp() * 1000)}'
                    }
                },
            }
        }
    
    load_restaurants = MongoFetchManyOperator(
        task_id='load_restaurants',
        mongo_conn_id='mongo_source',
        mongo_collection=MongoCollections.Restaurants.value,
        query_provider=query_provider_restaurants,
    )

    def process_restaurants(task_instance: TaskInstance):
        values: List[dict] = task_instance.xcom_pull(task_ids='load_restaurants')
        operations: List[str]

        from processors.mongo_processor import MongoProcessor
        mongo_processor = MongoProcessor()

        operations = list(
            map(
                lambda entry: mongo_processor.process_collection_entry_into_operation(
                    collection=MongoCollections.Restaurants,
                    entry=entry,
                ),
                values,
            )
        )

        Variable.set(
            key='MONGO__new_last_loaded_timestamp_restaurants',
            value=mongo_processor.get_latest_update_time().isoformat(),
            serialize_json=True
        )

        return ";".join(operations)
    process_restaurants_op = PythonOperator(task_id='process_restaurants', python_callable=process_restaurants)
    # ------------------------------------------------------------------------------------

    # --------------------------------------- loads orders -------------------------------
    def query_provider_orders() -> dict:
        return {
            "update_time": {
                "$gt": {
                    "$date": {
                        "$numberLong": f'{int(datetime.datetime.fromisoformat(Variable.get('MONGO__last_loaded_timestamp_orders', deserialize_json=True)).timestamp() * 1000)}'
                    }
                }
            }
        }
    
    load_orders = MongoFetchManyOperator(
        task_id='load_orders',
        mongo_conn_id='mongo_source',
        mongo_collection=MongoCollections.Orders.value,
        query_provider=query_provider_orders,
    )

    def process_orders(task_instance: TaskInstance):
        values: List[dict] = task_instance.xcom_pull(task_ids='load_orders')
        operations: List[str]

        from processors.mongo_processor import MongoProcessor
        mongo_processor = MongoProcessor()

        operations = list(
            map(
                lambda entry: mongo_processor.process_collection_entry_into_operation(
                    collection=MongoCollections.Orders,
                    entry=entry,
                ),
                values,
            )
        )

        Variable.set(
            key='MONGO__new_last_loaded_timestamp_orders',
            value=mongo_processor.get_latest_update_time().isoformat(),
            serialize_json=True
        )

        return ";".join(operations)
    process_orders_op = PythonOperator(task_id='process_orders', python_callable=process_orders)
    # ------------------------------------------------------------------------------------

    # --------------------------------------- loads clients ------------------------------
    def query_provider_clients() -> dict:
        return {
            "update_time": {
                "$gt": {
                    "$date": {
                        "$numberLong": f'{int(datetime.datetime.fromisoformat(Variable.get('MONGO__last_loaded_timestamp_clients', deserialize_json=True)).timestamp() * 1000)}'
                    }
                }
            }
        }

    load_clients = MongoFetchManyOperator(
        task_id='load_clients',
        mongo_conn_id='mongo_source',
        mongo_collection=MongoCollections.Clients.value,
        query_provider=query_provider_clients,
    )

    def process_clients(task_instance: TaskInstance):
        values: List[dict] = task_instance.xcom_pull(task_ids='load_clients')
        operations: List[str]

        from processors.mongo_processor import MongoProcessor
        mongo_processor = MongoProcessor()

        operations = list(
            map(
                lambda entry: mongo_processor.process_collection_entry_into_operation(
                    collection=MongoCollections.Clients,
                    entry=entry,
                ),
                values,
            )
        )

        Variable.set(
            key='MONGO__new_last_loaded_timestamp_clients',
            value=mongo_processor.get_latest_update_time().isoformat(),
            serialize_json=True
        )

        return ";".join(operations)
    process_clients_op = PythonOperator(task_id='process_clients', python_callable=process_clients)
    # ------------------------------------------------------------------------------------

    # --------------------------------------- save ---------------------------------------
    def prepare_data(task_instance: TaskInstance):
        restaurant_operations: str = task_instance.xcom_pull(task_ids='process_restaurants')
        order_operations: str = task_instance.xcom_pull(task_ids='process_orders')
        client_operations: str = task_instance.xcom_pull(task_ids='process_clients')

        all_operations: List[str] = [restaurant_operations, order_operations, client_operations]

        settings_initialized: bool = Variable.get('MONGO__settings_initialized', deserialize_json=True)

        new_last_loaded_timestamp_restaurants: datetime.datetime = datetime.datetime.fromisoformat(Variable.get('MONGO__new_last_loaded_timestamp_restaurants', deserialize_json=True))
        new_last_loaded_timestamp_orders: datetime.datetime = datetime.datetime.fromisoformat(Variable.get('MONGO__new_last_loaded_timestamp_orders', deserialize_json=True))
        new_last_loaded_timestamp_clients: datetime.datetime = datetime.datetime.fromisoformat(Variable.get('MONGO__new_last_loaded_timestamp_clients', deserialize_json=True))

        settings: dict = {
            'last_loaded_timestamp_restaurants': new_last_loaded_timestamp_restaurants.isoformat(),
            'last_loaded_timestamp_orders': new_last_loaded_timestamp_orders.isoformat(),
            'last_loaded_timestamp_clients': new_last_loaded_timestamp_clients.isoformat(),
        }

        import json
        settings_str: str = json.dumps(settings)

        if not settings_initialized:
            all_operations.append(f"""
                INSERT INTO staging.settings(source_id, settings) VALUES('MONGO', '{settings_str}')
            """)
        else:
            all_operations.append(f"""
                UPDATE staging.settings SET settings = '{settings_str}' WHERE source_id = 'MONGO'
            """)

        return ";".join(all_operations)
    prepare_data_op = PythonOperator(task_id='prepare_data', python_callable=prepare_data)

    save_changes_to_staging = SQLExecuteQueryOperator(
        task_id='save_changes_to_staging',
        conn_id='postgres_dwh',
        sql="{{ ti.xcom_pull(task_ids='prepare_data') }}"
    )
    # ------------------------------------------------------------------------------------

    load_settings >> process_settings_op >> [load_restaurants, load_orders, load_clients]
    load_restaurants >> process_restaurants_op
    load_orders >> process_orders_op
    load_clients >> process_clients_op
    [process_restaurants_op, process_orders_op, process_clients_op] >> prepare_data_op >> save_changes_to_staging


load_mongo_source_dag()
