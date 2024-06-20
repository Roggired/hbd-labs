import datetime
import json
from typing import List, Any

from airflow.decorators import dag
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.models.taskinstance import TaskInstance
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


@dag(
    dag_id='load_staging_source_dag',
    schedule_interval='@once',
    start_date=datetime.datetime(2024, 6, 18),
    catchup=False,
    tags=['load'],
    is_paused_upon_creation=False,
)
def staging_source_dag():
    # -------------------- Clearing dds
    clear_deliveries = SQLExecuteQueryOperator(
        task_id='clear_deliveries',
        conn_id='postgres_dwh',
        sql='DELETE FROM dds.dm_deliveryman;'
    )
    clear_deliverymen = SQLExecuteQueryOperator(
        task_id='clear_deliverymen',
        conn_id='postgres_dwh',
        sql='DELETE FROM dds.dm_deliveries;'
    )
    clear_payments = SQLExecuteQueryOperator(
        task_id='clear_payments',
        conn_id='postgres_dwh',
        sql='DELETE FROM dds.dm_payments;'
    )
    clear_orders = SQLExecuteQueryOperator(
        task_id='clear_orders',
        conn_id='postgres_dwh',
        sql='DELETE FROM dds.dm_orders;'
    )

    # -------------------- Loading orders
    load_orders = SQLExecuteQueryOperator(
        task_id='load_orders',
        conn_id='postgres_dwh',
        sql="SELECT * FROM staging.mongo_orders ORDER BY id ASC;"
    )

    # --------------------- Getting order ids
    def map_order_ids(task_instance: TaskInstance):
        operations: List[str] = list(
            map(
                lambda row: row[2]['_id'],
                task_instance.xcom_pull(task_ids='load_orders')
            )
        )

        joined_operations = "', '".join(operations)
        return f"('{joined_operations}')"

    process_orders_op = PythonOperator(task_id='map_order_ids', python_callable=map_order_ids)

    # ---------------------- Loading other entities
    load_payments = SQLExecuteQueryOperator(
        task_id='load_payments',
        conn_id='postgres_dwh',
        sql="SELECT * FROM staging.pg_payment WHERE order_id IN {{ task_instance.xcom_pull(task_ids='map_order_ids') }};"
    )

    load_deliveries = SQLExecuteQueryOperator(
        task_id='load_deliveries',
        conn_id='postgres_dwh',
        sql="SELECT * FROM staging.api_delivery WHERE order_id IN {{ task_instance.xcom_pull(task_ids='map_order_ids') }};"
    )

    def map_deliveryman_ids(task_instance: TaskInstance):
        operations: List[str] = list(
            map(
                lambda row: row[1],
                task_instance.xcom_pull(task_ids='load_deliveries')
            )
        )

        joined_operations = "', '".join(operations)
        return f"('{joined_operations}')"

    map_deliveryman_ids = PythonOperator(task_id='map_deliveryman_ids', python_callable=map_deliveryman_ids)

    load_deliveryman = SQLExecuteQueryOperator(
        task_id='load_deliveryman',
        conn_id='postgres_dwh',
        sql="SELECT * FROM staging.api_deliveryman WHERE id IN {{ task_instance.xcom_pull(task_ids='map_deliveryman_ids') }};"
    )

    # ------ Saving payments
    def process_payments(task_instance: TaskInstance):
        from processors.dds_processor import process_payment
        operations: List[str] = list(
            map(
                lambda row: process_payment(row),
                task_instance.xcom_pull(task_ids='load_payments')
            )
        )
        return ';'.join(operations)

    process_payments = PythonOperator(task_id='process_payments', python_callable=process_payments)

    save_payments = SQLExecuteQueryOperator(
        task_id='save_payments',
        conn_id='postgres_dwh',
        sql="{{ task_instance.xcom_pull(task_ids='process_payments') }};"
    )

    # ------ Saving deliveries
    def process_deliveries(task_instance: TaskInstance):
        from processors.dds_processor import process_delivery
        operations: List[str] = list(
            map(
                lambda row: process_delivery(row),
                task_instance.xcom_pull(task_ids='load_deliveries')
            )
        )
        return ';'.join(operations)

    process_deliveries = PythonOperator(task_id='process_deliveries', python_callable=process_deliveries)

    save_deliveries = SQLExecuteQueryOperator(
        task_id='save_deliveries',
        conn_id='postgres_dwh',
        sql="{{ task_instance.xcom_pull(task_ids='process_deliveries') }};"
    )

    # ------ Saving deliveryman
    def process_deliveryman(task_instance: TaskInstance):
        from processors.dds_processor import process_deliveryman
        operations: List[str] = list(
            map(
                lambda row: process_deliveryman(row),
                task_instance.xcom_pull(task_ids='load_deliveryman')
            )
        )
        return ';'.join(operations)

    process_deliveryman = PythonOperator(task_id='process_deliveryman', python_callable=process_deliveryman)

    save_deliveryman = SQLExecuteQueryOperator(
        task_id='save_deliveryman',
        conn_id='postgres_dwh',
        sql="{{ task_instance.xcom_pull(task_ids='process_deliveryman') }};"
    )

    # ---------------- Saving orders
    def process_dm_orders(task_instance: TaskInstance):
        payments: List[Any] = task_instance.xcom_pull(task_ids='load_payments')
        deliveries = task_instance.xcom_pull(task_ids='load_deliveries')
        deliverymen = task_instance.xcom_pull(task_ids='load_deliveryman')
        orders = task_instance.xcom_pull(task_ids='load_orders')

        from processors.dds_processor import process_order

        def process(row: List[Any]) -> str:
            delivery = [i for i in deliveries if row[1] == i[4]][0]
            return process_order(
                order=row,
                payment=[i for i in payments if row[1] == i[4]][0],
                delivery=delivery,
                deliveryman=[i for i in deliverymen if delivery[1] == i[0]][0],
            )

        operations: List[str] = list(
            map(
                lambda row: process(row),
                orders
            )
        )
        return ';'.join(operations)

    process_dm_orders = PythonOperator(task_id='process_dm_orders', python_callable=process_dm_orders)

    save_orders = SQLExecuteQueryOperator(
        task_id='save_orders',
        conn_id='postgres_dwh',
        sql="{{ task_instance.xcom_pull(task_ids='process_dm_orders') }};"
    )

    [clear_orders, clear_deliveries, clear_deliverymen, clear_payments] >> load_orders >> process_orders_op
    process_orders_op >> load_payments
    process_orders_op >> load_deliveries >> map_deliveryman_ids >> load_deliveryman
    load_payments >> process_payments >> save_payments
    load_deliveries >> process_deliveries >> save_deliveries
    load_deliveryman >> process_deliveryman >> save_deliveryman
    [save_payments, save_deliveries, save_deliveryman] >> process_dm_orders >> save_orders


staging_source_dag()
