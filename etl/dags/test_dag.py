import datetime

from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


@dag(
    dag_id="test_dag",
    schedule_interval='@hourly',
    start_date=datetime.datetime(2024, 6, 12, tzinfo=datetime.timezone.utc),
    catchup=False,
    tags=['test_dag'],
    is_paused_upon_creation=False,
)
def test_dag():
    SQLExecuteQueryOperator(
        task_id='test_task',
        conn_id='postgres_source',
        sql='SELECT version();'
    )


test_dag()
