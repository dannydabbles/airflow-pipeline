import airflow
from airflow import DAG
from datetime import timedelta
from airflow.operators.dummy_operator import DummyOperator


default_args =  {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

with DAG(
    'DUMMY_DAG',
    default_args=default_args,
    catchup=True, schedule_interval=None
) as dag:

    start = DummyOperator(
    task_id='start',
    dag=dag,
    )

start
