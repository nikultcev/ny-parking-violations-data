import requests
from airflow.exceptions import AirflowException

url = 'https://data.cityofnewyork.us/api/catalog/v1?search_context=data.ny.gov&Data-Collection_Data-Collection=DOF+Parking+Violations+Issued&names=Parking Violations Issued - Fiscal Year '

def search(
        year: int
    ):
    response = requests.get(
        url=f'{url}{year}'
    )
    response.raise_for_status()

    try:
        return response.json()['results'][0]['resource']['id']
    except Exception as e:
        raise AirflowException(f"Error getting the requested dataset id: {e}")
