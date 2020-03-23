FROM astronomerinc/ap-airflow:1.10.7-alpine3.10

COPY plugins /usr/local/airflow/plugins
COPY dags /usr/local/airflow/dags
