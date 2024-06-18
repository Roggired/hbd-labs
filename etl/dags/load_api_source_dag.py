import datetime
import pytz
from typing import Any, List, Dict

from airflow.decorators import dag
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.models.taskinstance import TaskInstance
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from operators.api_operator import APIFetchOperator


@dag(
    dag_id="load_api_source_dag",
    schedule_interval='*/5 * * * *',
    start_date=datetime.datetime(2024, 6, 16),
    catchup=False,
    tags=['load'],
    is_paused_upon_creation=False,
)
def load_api_source_dag():
    # --------------------------------------- settings -----------------------------------
    load_settings = SQLExecuteQueryOperator(
        task_id='load_settings',
        conn_id='postgres_dwh',
        sql="SELECT settings FROM staging.settings WHERE source_id = 'API';"
    )

    def process_settings(task_instance: TaskInstance):
        values: List[List[Any]] = task_instance.xcom_pull(task_ids='load_settings')
        settings: Dict[str, Any]
        if len(values) <= 0:
            settings = {
                'last_loaded_timestamp_deliveries': datetime.datetime(1900, 1, 1, tzinfo=pytz.utc),
            }
            Variable.set(
                key='API__settings_initialized',
                value=False,
                serialize_json=True
            )
        else:
            settings_raw = values[0][0]
            settings = {
                'last_loaded_timestamp_deliveries': datetime.datetime.fromisoformat(settings_raw['last_loaded_timestamp_deliveries']),
            }
            Variable.set(
                key='API__settings_initialized',
                value=True,
                serialize_json=True
            )

        Variable.set(
            key='API__last_loaded_timestamp_deliveries',
            value=settings['last_loaded_timestamp_deliveries'].isoformat(),
            serialize_json=True
        )
        return settings

    process_settings_op = PythonOperator(task_id='process_settings', python_callable=process_settings)

    load_number_of_deliverymans = SQLExecuteQueryOperator(
        task_id='load_number_of_deliveryman',
        conn_id='postgres_dwh',
        sql="SELECT COUNT(*) FROM staging.api_deliveryman;"
    )

    def process_number_of_deliverymans(task_instance: TaskInstance):
        number: List[List[int]] = task_instance.xcom_pull(task_ids='load_number_of_deliveryman')
        Variable.set(
            key="API__number_of_deliverymans",
            value=number,
            serialize_json=True
        )
        return number
    process_number_of_deliverymans_op = PythonOperator(task_id='process_number_of_deliverymans', python_callable=process_number_of_deliverymans)
    # ------------------------------------------------------------------------------------

    # --------------------------------------- loads deliveries ---------------------------
    def load_deliveries_body_provider():
        return {
            'delivery_time_filter_clause': Variable.get(key='API__last_loaded_timestamp_deliveries', deserialize_json=True),
        }

    load_deliveries = APIFetchOperator(
        task_id='load_deliveries',
        conn_variable_id='api_delivery',
        query_params={
            'page_number': 0,
            'page_size': 100,
        },
        body_provider=load_deliveries_body_provider,
    )

    def process_deliveries(task_instance: TaskInstance):
        page: dict = task_instance.xcom_pull(task_ids='load_deliveries')
        if page.get('content', None) is None:
            return ""

        content: List[dict] = page['content']
        if len(content) == 0:
            return ""

        from processors.api_processor import APIProcessor
        api_processor = APIProcessor()

        operations: List[str] = list(
            map(
                lambda entity: api_processor.process_delivery(entity),
                content,
            )
        )

        Variable.set(
            key='API__new_last_loaded_timestamp_deliveries',
            value=api_processor.get_last_delivery_time().isoformat(),
            serialize_json=True,
        )

        return ";".join(operations)
    process_deliveries_op = PythonOperator(task_id='process_deliveries', python_callable=process_deliveries)
    # ------------------------------------------------------------------------------------

    # --------------------------------------- loads deliverymans -------------------------
    def load_deliverymans_body_provider():
        return {
            'number_of_deliverymans_to_skip': Variable.get(key='API__number_of_deliverymans', deserialize_json=True)[0][0],
        }

    load_deliverymans = APIFetchOperator(
        task_id='load_deliverymans',
        conn_variable_id='api_deliveryman',
        query_params={
            'page_number': 0,
            'page_size': 100,
        },
        body_provider=load_deliverymans_body_provider,
    )

    def process_deliverymans(task_instance: TaskInstance):
        page: dict = task_instance.xcom_pull(task_ids='load_deliverymans')
        if page.get('content', None) is None:
            return ""

        content: List[dict] = page['content']
        if len(content) == 0:
            return ""

        from processors.api_processor import APIProcessor
        api_processor = APIProcessor()

        operations: List[str] = list(
            map(
                lambda entity: api_processor.process_deliveryman(entity),
                content,
            )
        )

        return ";".join(operations)
    process_deliverymans_op = PythonOperator(task_id='process_deliverymans', python_callable=process_deliverymans)
    # ------------------------------------------------------------------------------------

    # --------------------------------------- save ---------------------------------------
    def prepare_data(task_instance: TaskInstance):
        deliveries_operations: str = task_instance.xcom_pull(task_ids='process_deliveries')
        deliverymans_operations: str = task_instance.xcom_pull(task_ids='process_deliverymans')

        all_operations: List[str] = [deliveries_operations, deliverymans_operations]

        settings_initialized: bool = Variable.get('API__settings_initialized', deserialize_json=True)

        new_last_loaded_timestamp_deliveries: datetime.datetime = datetime.datetime.fromisoformat(Variable.get('API__new_last_loaded_timestamp_deliveries', deserialize_json=True))

        settings: dict = {
            'last_loaded_timestamp_deliveries': new_last_loaded_timestamp_deliveries.isoformat(),
        }

        import json
        settings_str: str = json.dumps(settings)

        if not settings_initialized:
            all_operations.append(f"""
                INSERT INTO staging.settings(source_id, settings) VALUES('API', '{settings_str}')
            """)
        else:
            all_operations.append(f"""
                UPDATE staging.settings SET settings = '{settings_str}' WHERE source_id = 'API'
            """)

        return ";".join(all_operations)
    prepare_data_op = PythonOperator(task_id='prepare_data', python_callable=prepare_data)

    save_changes_to_staging = SQLExecuteQueryOperator(
        task_id='save_changes_to_staging',
        conn_id='postgres_dwh',
        sql="{{ ti.xcom_pull(task_ids='prepare_data') }}"
    )
    # ------------------------------------------------------------------------------------

    load_settings >> process_settings_op >> load_deliveries >> process_deliveries_op
    load_number_of_deliverymans >> process_number_of_deliverymans_op >> load_deliverymans >> process_deliverymans_op
    [process_deliveries_op, process_deliverymans_op] >> prepare_data_op >> save_changes_to_staging


load_api_source_dag()
