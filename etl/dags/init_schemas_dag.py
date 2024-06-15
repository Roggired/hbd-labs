import datetime

from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


@dag(
    dag_id="init_schemas",
    schedule_interval='@once',
    start_date=datetime.datetime.now(),
    catchup=False,
    tags=['init_schemas'],
    is_paused_upon_creation=False,
)
def init_schemas_dag():
    init_staging_schema = SQLExecuteQueryOperator(
        task_id='init_staging_schema',
        conn_id='postgres_dwh',
        sql='ddl/staging.sql'
    )

    init_dds_schema = SQLExecuteQueryOperator(
        task_id='init_dds_schema',
        conn_id='postgres_dwh',
        sql='ddl/dds.sql'
    )

    init_cdm_schema = SQLExecuteQueryOperator(
        task_id='init_cdm_schema',
        conn_id='postgres_dwh',
        sql='ddl/cdm.sql'
    )

    init_staging_schema >> init_dds_schema >> init_cdm_schema


init_schemas_dag()
