from airflow.decorators import dag,task
from upload_to_datalake import upload
from datetime import datetime,timedelta
from find_dataset_id import search
from download_from_datalake import download
from transform_upload_to_dwh import read_transform_upload
from delete_temp_file import delete
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

@dag(
    dag_id='upload_raw_violations',
    # We run this script every year starting from 1 July, the end of Fiscal year in NY, when the city is expected to publish the dataset
    schedule="0 0 1 7 *",
    start_date=datetime(2014,1,1),
    catchup=True,
    default_args={
        "retries":12,
        #We retry every week to check is the city has published the dataset
        "retry_delay": timedelta(weeks=1)
    },
    max_active_runs=1
)
def taskflow():

    @task()
    def find_dataset_id(**context):
        #Extract year from the dag run date
        year = datetime.fromisoformat(context['ts']).year
        dataset_id = search(year)

        return {"year": year, "dataset_id": dataset_id}
    
    @task()
    def upload_raw_to_datalake(
        metadata: dict,
    ):
        year = metadata['year']
        dataset_id = metadata['dataset_id']

        file_name = f'raw_{year}_data.csv'

        upload(
            dataset_id=dataset_id,
            file_name=file_name
        )

        return file_name

    @task()
    def download_raw_from_datalake(
        file_name
    ):
        download(file_name)
    
    @task()
    def transform_upload_to_dwh(
        file_name: str,
        metadata: dict
    ):
        year = metadata['year']
        read_transform_upload(file_name,year)

    @task()
    def delete_temp_file(
        file_name: str
    ):
        delete(file_name)

    run_dbt = TriggerDagRunOperator(
        task_id='run_dbt',
        trigger_dag_id='run_dbt_models',
        wait_for_completion=True
    )

    dataset_metadata = find_dataset_id()
    file_name = upload_raw_to_datalake(dataset_metadata)

    dataset_metadata>>file_name>>download_raw_from_datalake(file_name)>>transform_upload_to_dwh(file_name,dataset_metadata)>>delete_temp_file(file_name)>>run_dbt

    

taskflow()