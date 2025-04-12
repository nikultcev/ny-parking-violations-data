import pandas as pd
import numpy as np
import os
from upload_to_dwh import upload
import logging


def transform(
        data: pd.DataFrame,
        year: int
    )->pd.DataFrame:

    #Rename to the same uniform naming convention
    columns = {
        "Summons Number":"summons_number",
        "Plate ID":"plate_id",
        "Registration State":"registration",
        "Plate Type":"plate_type",
        "Issue Date":"issue_date",
        "Violation Code":"violation_code",
        "Vehicle Body Type":"vehicle_body_type",
        "Vehicle Make":"vehicle_make",
        "Issuing Agency":"issuing_agency",
        "Street Code1":"street_code1",
        "Street Code2":"street_code2",
        "Street Code3":"street_code3",
        "Vehicle Expiration Date":"vehicle_expiration_date",
        "Violation Location":"violation_location",
        "Violation Precinct":"violation_precinct",
        "Issuer Precinct":"issuer_precinct",
        "Issuer Code":"issuer_code",
        "Issuer Command":"issuer_command",
        "Issuer Squad":"issuer_squad",
        "Violation Time":"violation_time",
        "Time First Observed":"time_first_observed",
        "Violation County":"violation_county",
        "Violation In Front Of Or Opposite":"is_violation_in_front",
        "House Number": "house_number",
        "Street Name": "street_name",
        "Number":"house_number",
        "Street":"street_name",
        "Intersecting Street":"intersecting_street",
        "Date First Observed":"date_first_observed",
        "Law Section":"law_section",
        "Sub Division":"sub_division",
        "Violation Legal Code":"violation_legal_code",
        "Days Parking In Effect":"days_parking_in_effect",
        "From Hours In Effect":"from_hours_in_effect",
        "To Hours In Effect":"to_hours_in_effect",
        "Vehicle Color":"vehicle_color",
        "Unregistered Vehicle?":"is_vehicle_unregistered",
        "Vehicle Year":"vehicle_year",
        "Meter Number":"meter_number",
        "Feet From Curb":"feet_from_curb",
        "Violation Post Code":"violation_post_code",
        "Violation Description":"violation_description",
        "No Standing or Stopping Violation":"no_standing_or_stopping_violation",
        "Hydrant Violation":"hydrant_violation",
        "Double Parking Violation":"double_parking_violation"
    }

    #Specify data types so we would not get any errors because of mixed data types
    dtypes = {
        "summons_number":"Int64",
        "plate_id":"string",
        "registration":"string",
        "plate_type":"string",
        "violation_code":"Int64",
        "vehicle_body_type":"string",
        "vehicle_make":"string",
        "issuing_agency":"string",
        "street_code1":"Int64",
        "street_code2":"Int64",
        "street_code3":"Int64",
        "violation_location":"Int64",
        "violation_precinct":"Int64",
        "issuer_precinct":"Int64",
        "issuer_code":"Int64",
        "issuer_command":"string",
        "issuer_squad":"string",
        "violation_county":"string",
        "house_number":"string",
        "street_name":"string",
        "intersecting_street":"string",
        "sub_division":"string",
        "violation_legal_code":"string",
        "days_parking_in_effect":"string",
        "from_hours_in_effect":"string",
        "to_hours_in_effect":"string",
        "vehicle_color":"string",
        "violation_description":"string",
        "no_standing_or_stopping_violation":"string",
        "hydrant_violation":"string",
        "double_parking_violation":"string",
        "time_first_observed":"string",
        "violation_time":"string",
        "meter_number":"string",
        "law_section":"Int64",
        "vehicle_year":"Int64",
        "feet_from_curb":"Int64",
        "is_vehicle_unregistered":"bool",
        "is_violation_in_front":"bool",
        "violation_post_code":"string",
        "violation_legal_code":"string"
    }

    # Some columns might have tabs and spaces in their names, so we clean before renaming with dictionary
    data.columns = data.columns.str.strip()
    data = data.rename(columns=columns)
    data['dataset_year'] = year

    #Replace zeroes with null as these values are not valid for these columns
    data[['vehicle_year',
        'street_code1',
        'street_code2',
        'street_code3',
        'vehicle_expiration_date',
        'issuer_code',
        'date_first_observed',
        'law_section',
        'feet_from_curb',
        'violation_precinct',
        'issuer_precinct']]=data[['vehicle_year',
                                    'street_code1',
                                    'street_code2',
                                    'street_code3',
                                    'vehicle_expiration_date',
                                    'issuer_code',
                                    'date_first_observed',
                                    'law_section',
                                    'feet_from_curb',
                                    'violation_precinct',
                                    'issuer_precinct']].replace(to_replace=0,value=np.nan,regex=True)

    #Transform to boolean column
    data.is_violation_in_front=data.is_violation_in_front.replace({'F':1,'O':0})
    data[['issuer_command','issuer_squad']]=data[['issuer_command','issuer_squad']].replace(to_replace=[r"^0000$",0],value=np.nan,regex=True)

    data['meter_number']=data['meter_number'].replace(to_replace=r"^-$",value=np.nan,regex=True)

    data = data.astype(dtype=dtypes,errors='raise')

    data.date_first_observed=data.date_first_observed.replace('01/05/0001 12:00:00 PM',np.nan)

    data['violation_time']=data['violation_time'].str.replace('A', 'AM').str.replace('P', 'PM')
    data['time_first_observed']=data['time_first_observed'].str.replace('A', 'AM').str.replace('P', 'PM')

    data[['vehicle_expiration_date','date_first_observed']]=data[['vehicle_expiration_date','date_first_observed']].apply(pd.to_datetime,format="%Y%m%d",errors='coerce')

    data.issue_date = pd.to_datetime(data.issue_date)

    data[['violation_time','time_first_observed']]=data[['violation_time','time_first_observed']].apply(pd.to_datetime,format="%I%M%p",errors='coerce')

    logging.info(f"Transformed {len(data)} rows")

    return data

def read_transform_upload(
        file_name:str,
        year: int
    )->None:

    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_dir = os.path.join(script_dir, "temp")
    local_path = os.path.join(local_dir, file_name)

    for chunk in pd.read_csv(local_path,chunksize=100000):
        transformed_chunk = transform(chunk, year)
        upload(transformed_chunk)
