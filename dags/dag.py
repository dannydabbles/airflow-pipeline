import airflow
from airflow import DAG
from datetime import timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.utils.trigger_rule import TriggerRule

from bs4 import BeautifulSoup
import requests

default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

with DAG(
        'save_web_text',
        default_args=default_args,
        catchup=True, schedule_interval=None
) as dag:
    def download_webpage(**context):
        # Make a GET request to fetch the raw HTML content
        html_content = requests.get(context['params']['url']).text
        return html_content


    download_webpage = PythonOperator(
        task_id='download_webpage',
        provide_context=True,
        python_callable=download_webpage,
        dag=dag,
    )


    def strip_html_tags(ds, **kwargs):
        ti = kwargs['ti']
        html_content = ti.xcom_pull(task_ids='download_webpage')
        soup = BeautifulSoup(html_content)
        text = soup.get_text()
        return text


    strip_html_tags = PythonOperator(
        task_id='strip_html_tags',
        provide_context=True,
        python_callable=strip_html_tags,
        dag=dag,
    )


    def convert_text_upper_case(ds, **kwargs):
        ti = kwargs['ti']
        text = ti.xcom_pull(task_ids='strip_html_tags')
        return text.upper()


    convert_text_upper_case = PythonOperator(
        task_id='convert_text_upper_case',
        provide_context=True,
        python_callable=convert_text_upper_case,
        dag=dag,
    )

    create_table = PostgresOperator(
        task_id='create_table',
        provide_context=True,
        sql="""CREATE TABLE IF NOT EXISTS save_web_text (
            id SERIAL PRIMARY KEY,
            url VARCHAR(255) NOT NULL,
            text TEXT
        );
        """,
        trigger_rule=TriggerRule.ALL_DONE,
    )

    persist_results = PostgresOperator(
        task_id='persist_results',
        provide_context=True,
        sql="INSERT INTO save_web_text (url, text) VALUES(" + \
            "'{{params.url}}'" + ", " + \
            """'{{ti.xcom_pull(task_ids='convert_text_upper_case') | replace("'", "''")}}'""" + ")",
        trigger_rule=TriggerRule.ALL_DONE,
    )

download_webpage >> strip_html_tags >> convert_text_upper_case >> create_table >> persist_results
