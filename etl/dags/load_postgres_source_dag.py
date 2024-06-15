import datetime
from typing import Any, List

from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.models.taskinstance import TaskInstance
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


# TODO: incremental data loading
@dag(
    dag_id="load_postgres_source",
    schedule_interval='@once',
    start_date=datetime.datetime.now(),
    catchup=False,
    tags=['load'],
    is_paused_upon_creation=False,
)
def load_postgres_source_dag():
    # --------------------------------------- dish ---------------------------------------
    load_dish_from_source = SQLExecuteQueryOperator(
        task_id='load_dish_from_source',
        conn_id='postgres_source',
        sql='SELECT * FROM dish;'
    )

    def process_dish(task_instance: TaskInstance):
        values: List[Any] = task_instance.xcom_pull(task_ids='load_dish_from_source')
        values_prepared: List[str] = []

        for value in values:
            values_prepared.append(f"""
                (
                    {value[0]},
                    '{value[1]}',
                    {value[2]},
                    null,
                    null,
                    now()
                )
            """)

        return ",".join(values_prepared)
    process_dish_op = PythonOperator(task_id='process_dish', python_callable=process_dish)

    save_dish_to_staging = SQLExecuteQueryOperator(
        task_id='save_dish_to_staging',
        conn_id='postgres_dwh',
        sql="INSERT INTO staging.pg_dish(dish_id, name, price, when_created, when_updated, when_uploaded) VALUES {{ ti.xcom_pull(task_ids='process_dish') }}"
    )
    # ------------------------------------------------------------------------------------
    
    # --------------------------------------- category -----------------------------------
    load_category_from_source = SQLExecuteQueryOperator(
        task_id='load_category_from_source',
        conn_id='postgres_source',
        sql='SELECT * FROM category;'
    )

    def process_category(task_instance: TaskInstance):
        values: List[Any] = task_instance.xcom_pull(task_ids='load_category_from_source')
        values_prepared: List[str] = []

        for value in values:
            values_prepared.append(f"""
                (
                    {value[0]},
                    '{value[1]}',
                    {value[2]},
                    {value[3]},
                    null,
                    null,
                    now()
                )
            """)

        return ",".join(values_prepared)
    process_category_op = PythonOperator(task_id='process_category', python_callable=process_category)

    save_category_to_staging = SQLExecuteQueryOperator(
        task_id='save_category_to_staging',
        conn_id='postgres_dwh',
        sql="INSERT INTO staging.pg_category(category_id, name, percent, min_payment, when_created, when_updated, when_uploaded) VALUES {{ ti.xcom_pull(task_ids='process_category') }}"
    )
    # ------------------------------------------------------------------------------------
    
    # --------------------------------------- client -----------------------------------
    load_client_from_source = SQLExecuteQueryOperator(
        task_id='load_client_from_source',
        conn_id='postgres_source',
        sql='SELECT * FROM client;'
    )

    def process_client(task_instance: TaskInstance):
        values: List[Any] = task_instance.xcom_pull(task_ids='load_client_from_source')
        values_prepared: List[str] = []

        for value in values:
            values_prepared.append(f"""
                (
                    {value[0]},
                    {value[1]},
                    {value[2]},
                    null,
                    null,
                    now()
                )
            """)

        return ",".join(values_prepared)
    process_client_op = PythonOperator(task_id='process_client', python_callable=process_client)

    save_client_to_staging = SQLExecuteQueryOperator(
        task_id='save_client_to_staging',
        conn_id='postgres_dwh',
        sql="INSERT INTO staging.pg_client(client_id, bonus_balance, category_id, when_created, when_updated, when_uploaded) VALUES {{ ti.xcom_pull(task_ids='process_client') }}"
    )
    # ------------------------------------------------------------------------------------
    
    # --------------------------------------- payment -----------------------------------
    load_payment_from_source = SQLExecuteQueryOperator(
        task_id='load_payment_from_source',
        conn_id='postgres_source',
        sql='SELECT * FROM payment;'
    )

    def process_payment(task_instance: TaskInstance):
        values: List[Any] = task_instance.xcom_pull(task_ids='load_payment_from_source')
        values_prepared: List[str] = []

        for value in values:
            values_prepared.append(f"""
                (
                    {value[0]},
                    {value[1]},
                    {value[2]},
                    {value[3]},
                    '{value[4]}',
                    '{value[5]}',
                    {value[6]},
                    {value[7]},
                    null,
                    null,
                    now()
                )
            """)

        return ",".join(values_prepared)
    process_payment_op = PythonOperator(task_id='process_payment', python_callable=process_payment)

    save_payment_to_staging = SQLExecuteQueryOperator(
        task_id='save_payment_to_staging',
        conn_id='postgres_dwh',
        sql="INSERT INTO staging.pg_payment(payment_id, client_id, dish_id, dish_amount, order_id, order_time, order_sum, tips, when_created, when_updated, when_uploaded) VALUES {{ ti.xcom_pull(task_ids='process_payment') }}"
    )
    # ------------------------------------------------------------------------------------

    load_dish_from_source >> process_dish_op >> save_dish_to_staging
    load_category_from_source >> process_category_op >> save_category_to_staging
    load_client_from_source >> process_client_op >> save_client_to_staging
    load_payment_from_source >> process_payment_op >> save_payment_to_staging


load_postgres_source_dag()
