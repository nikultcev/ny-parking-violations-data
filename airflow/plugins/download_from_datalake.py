import os
import logging
from airflow.providers.google.cloud.hooks.gcs import GCSHook
import os

BUCKET_NAME = os.environ.get('GOOGLE_CLOUD_STORAGE_BUCKET')

def download(file_name: str):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_dir = os.path.join(script_dir, "temp")
    local_path = os.path.join(local_dir, file_name)

    os.makedirs(local_dir, exist_ok=True)

    connection = GCSHook(gcp_conn_id="Google")
    blob = connection.get_conn().bucket(BUCKET_NAME).blob(file_name)

    blob.download_to_filename(local_path)
    logging.info(f"Finished downloading {file_name} to {local_path}")