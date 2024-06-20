import datetime
import pytz
import json
from typing import List, Any

from airflow.decorators import dag
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.models.taskinstance import TaskInstance
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


@dag(
    dag_id="load_dds_source_dag",
    schedule_interval='@once',
    start_date=datetime.datetime(2024, 6, 19),
    catchup=False,
    tags=['load'],
    is_paused_upon_creation=False,
)
def load_dds_source_dag():
    # ------------------------------- setup ---------------------------------
    def load_settings(task_instance: TaskInstance):
        date = datetime.datetime.now(tz=pytz.utc)
        year = date.year
        if date.day < 21:
            month = date.month - 1
        else:
            month = date.month
        day = date.day
        
        date_config: dict = {
            'year': year,
            'month': month,
            'day': day,
        } 
        Variable.set(
            key='CDM__target_date_config',
            value=date_config,
            serialize_json=True,
        )
        return date_config
    load_settings_op = PythonOperator(task_id='load_settings', python_callable=load_settings)

    clear_cdm = SQLExecuteQueryOperator(
        task_id='clear_cdm',
        conn_id='postgres_dwh',
        sql="DELETE FROM cdm.deliveryman_income WHERE year = {{ ti.xcom_pull(task_ids='load_settings')['year'] }} and month = {{ ti.xcom_pull(task_ids='load_settings')['month'] }};"
    )
    # -----------------------------------------------------------------------

    # ------------------------------- load payments -------------------------
    load_payments = SQLExecuteQueryOperator(
        task_id='load_payments',
        conn_id='postgres_dwh',
        sql="SELECT * FROM dds.dm_payments WHERE payment_year = {{ ti.xcom_pull(task_ids='load_settings')['year'] }} AND payment_month = {{ ti.xcom_pull(task_ids='load_settings')['month'] }};"
    )
    # -----------------------------------------------------------------------

    # ------------------------------- load orders ---------------------------
    def map_orders(task_instance: TaskInstance):
        payments: List[List] = task_instance.xcom_pull(task_ids='load_payments')
        from processors.cdm_processor import process_payment
        return process_payment(payments)
    map_orders_op = PythonOperator(task_id='map_orders', python_callable=map_orders)

    load_orders = SQLExecuteQueryOperator(
        task_id='load_orders',
        conn_id='postgres_dwh',
        sql="{{ task_instance.xcom_pull(task_ids='map_orders') }};"
    )
    # -----------------------------------------------------------------------

    # ------------------------------- load deliverymans & deliveries --------
    def fetch_ids_from_order(task_instance: TaskInstance):
        orders = task_instance.xcom_pull(task_ids='load_orders')
        deliveryman = list(map(
            lambda d: f"'{d[1]}'",
            orders
        ))
        return {
            'delivery_ids': ",".join(
                list(
                    map(
                        lambda el: f"'{el[3]}'",
                        orders
                    )
                )
            ),
            'sql': ','.join(deliveryman)
        }
    fetch_ids_from_order_op = PythonOperator(task_id='fetch_ids_from_order', python_callable=fetch_ids_from_order)

    load_deliverymans = SQLExecuteQueryOperator(
        task_id='load_deliverymans',
        conn_id='postgres_dwh',
        sql="SELECT * FROM dds.dm_deliveryman WHERE deliveryman_id IN ({{task_instance.xcom_pull(task_ids='fetch_ids_from_order')['sql']}});"
    )

    load_deliveries = SQLExecuteQueryOperator(
        task_id='load_deliveries',
        conn_id='postgres_dwh',
        sql="SELECT * FROM dds.dm_deliveries WHERE id IN ({{ ti.xcom_pull(task_ids='fetch_ids_from_order')['delivery_ids'] }})"
    )
    # -----------------------------------------------------------------------
    
    # ------------------------------- save to cdm ---------------------------
    def prepare_data(task_instance: TaskInstance):
        payments: List[List] = task_instance.xcom_pull(task_ids='load_payments')
        orders: List[List] = task_instance.xcom_pull(task_ids='load_orders')
        deliverymans: List[List] = task_instance.xcom_pull(task_ids='load_deliverymans')
        deliveries: List[List] = task_instance.xcom_pull(task_ids='load_deliveries')

        from processors.cdm_processor import process_data_from_dds
        return ";".join(process_data_from_dds(
            payments_raw=payments,
            orders_raw=orders,
            deliverymans_raw=deliverymans,
            deliveries_raw=deliveries,
        ))
    prepare_data_op = PythonOperator(task_id='prepare_data', python_callable=prepare_data)

    save_changes_to_cdm = SQLExecuteQueryOperator(
        task_id='save_changes_to_cdm',
        conn_id='postgres_dwh',
        sql='{{ ti.xcom_pull(task_ids="prepare_data") }}'
    )
    # -----------------------------------------------------------------------

    load_settings_op >> [clear_cdm, load_payments] >> map_orders_op >> load_orders >> fetch_ids_from_order_op >> [load_deliverymans, load_deliveries]
    [load_payments, load_orders, load_deliverymans, load_deliveries] >> prepare_data_op >> save_changes_to_cdm


load_dds_source_dag()
