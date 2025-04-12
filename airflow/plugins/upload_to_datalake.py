import requests
import logging
from airflow.providers.google.cloud.hooks.gcs import GCSHook
import os

CACHE_SIZE_MB = 5
MAX_SIZE_MB = int(os.environ['MAX_RAW_FILE_SIZE_MB'])

CACHE_SIZE_BYTES = CACHE_SIZE_MB * 1024 * 1024
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

def upload(dataset_id: str, file_name: str):
    bucket_name = "raw-data-bucket-ny-parking-violations-data"
    connection = GCSHook(gcp_conn_id="Google")

    url = f"https://data.cityofnewyork.us/api/views/{dataset_id}/rows.csv?accessType=DOWNLOAD&api_foundry=true"

    logging.info(f"Downloading {file_name} from {url}")

    logging.info(f"Cache size: {CACHE_SIZE_BYTES} bytes ({CACHE_SIZE_MB} MB)")
    logging.info(f"Маx file size for testing purposes {MAX_SIZE_BYTES} ({MAX_SIZE_MB} MB) ")

    #Instead of trying to download the whole file to the memory, we stream the file directly to the cloud in small batches
    with requests.get(url=url, stream=True) as response:
        response.raise_for_status()
        downloaded = 0

        blob = connection.get_conn().bucket(bucket_name).blob(file_name)
        blob.chunk_size = CACHE_SIZE_BYTES

        with blob.open("wb") as writer:

            for chunk in response.iter_content(chunk_size=CACHE_SIZE_BYTES):
                
                #For testing purposes we limit the maximum file size
                if downloaded + len(chunk) > MAX_SIZE_BYTES:

                    writer.write(chunk[: MAX_SIZE_BYTES - downloaded])
                    downloaded += len(chunk[: MAX_SIZE_BYTES - downloaded])

                    logging.info(f"Uploaded {downloaded / 1024 / 1024:.2f} MB")
                    break
                
                writer.write(chunk)
                downloaded += len(chunk)
                
                logging.info(f"Uploaded {downloaded / 1024 / 1024:.2f} MB")

    logging.info(f"Finished uploading {file_name}")