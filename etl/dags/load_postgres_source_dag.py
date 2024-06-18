import datetime
from typing import Any, List, Dict

from airflow.decorators import dag
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.models.taskinstance import TaskInstance
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


@dag(
    dag_id="load_postgres_source",
    schedule_interval='*/1 * * * *',
    start_date=datetime.datetime(2024, 6, 16),
    catchup=False,
    tags=['load'],
    is_paused_upon_creation=False,
)
def load_postgres_source_dag():
    # --------------------------------------- settings -----------------------------------
    load_settings = SQLExecuteQueryOperator(
        task_id='load_settings',
        conn_id='postgres_dwh',
        sql="SELECT settings FROM staging.settings WHERE source_id = 'POSTGRES';"
    )

    def process_settings(task_instance: TaskInstance):
        values: List[List[Any]] = task_instance.xcom_pull(task_ids='load_settings')
        settings: Dict[str, Any]
        if len(values) <= 0:
            settings = {
                'last_loaded_log_id': 0
            }
            Variable.set(
                key='POSTGRES__settings_initialized',
                value=False,
                serialize_json=True
            )
        else:
            settings = values[0][0]
            Variable.set(
                key='POSTGRES__settings_initialized',
                value=True,
                serialize_json=True
            )

        Variable.set(
            key='POSTGRES__last_loaded_log_id',
            value=settings['last_loaded_log_id'],
        )
        return settings['last_loaded_log_id']
    process_settings_op = PythonOperator(task_id='process_settings', python_callable=process_settings)
    # ------------------------------------------------------------------------------------

    # --------------------------------------- logs ---------------------------------------
    load_logs = SQLExecuteQueryOperator(
        task_id='load_logs',
        conn_id='postgres_source',
        sql="SELECT * FROM logs WHERE id > {{ ti.xcom_pull(task_ids='process_settings') }} ORDER BY id ASC LIMIT 100;"
    )

    def process_logs(task_instance: TaskInstance):
        values: List[Any] = task_instance.xcom_pull(task_ids='load_logs')
        operations: List[str]
        last_loaded_log_id = int(Variable.get(key='POSTGRES__last_loaded_log_id'))
        settings_initialized: bool = Variable.get(key='POSTGRES__settings_initialized', deserialize_json=True)

        from processors.postgres_processor import PostgresProcessor
        import json
        postgres_processor = PostgresProcessor(last_loaded_log_id)

        operations = list(
            map(
                lambda row: postgres_processor.process_log_row_into_operation(row),
                values,
            )
        )

        updated_settings: Dict[str, Any] = {
            'last_loaded_log_id': postgres_processor.get_last_processed_log_id()
        }
        if not settings_initialized:
            operations.append(
                f"INSERT INTO staging.settings(source_id, settings) VALUES('POSTGRES', '{json.dumps(updated_settings)}')"
            )
        else:
            operations.append(
                f"UPDATE staging.settings SET settings = '{json.dumps(updated_settings)}' WHERE source_id = 'POSTGRES'"
            )

        return ';'.join(operations)
    process_logs_op = PythonOperator(task_id='process_logs', python_callable=process_logs)

    save_changes_to_staging = SQLExecuteQueryOperator(
        task_id='save_changes_to_staging',
        conn_id='postgres_dwh',
        sql="{{ ti.xcom_pull(task_ids='process_logs') }}"
    )
    # ------------------------------------------------------------------------------------

    load_settings >> process_settings_op >> load_logs >> process_logs_op >> save_changes_to_staging


load_postgres_source_dag()
