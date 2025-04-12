select
    dataset_year,
    violation_code,
    summons_number,
    initcap(trim(street_name)) as street_name,
    trim(house_number) as house_number
from {{source('raw','violations')}}
where
    --Filter out invalid tickets where issue date is outside of dataset's fiscal year
    issue_date >= date(dataset_year-1,7,1) and
    issue_date <= date(dataset_year,6,30)