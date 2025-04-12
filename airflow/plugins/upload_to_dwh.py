import pandas as pd
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from pandas_gbq import to_gbq
import os

PROJECT_ID = os.environ.get('GOOGLE_PROJECT')

def upload(
        data: pd.DataFrame
    )->None:

    bq_hook = BigQueryHook(gcp_conn_id="Google-BigQuery")
    credentials = bq_hook.get_credentials()

    dataset_table = "raw.violations"

    to_gbq(data, dataset_table, project_id=PROJECT_ID, credentials=credentials, if_exists="append")