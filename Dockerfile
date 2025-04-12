FROM apache/airflow:2.10.5
USER root 
RUN apt-get update && apt-get install -y git && apt-get clean
USER airflow
COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}"
RUN pip install --no-cache-dir dbt-core dbt-bigquery