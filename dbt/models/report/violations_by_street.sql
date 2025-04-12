select 
    dataset_year,
    street_name,
    house_number,
    'USA' as country,
    'New York' as city,
    --Generate full address for Looker Map visual
    concat('USA New York ',street_name,' ',coalesce(house_number,'')) as full_address,
    count(summons_number) as violations,
    round(count(summons_number)/sum(count(summons_number)) OVER (),2) as violations_share_of_total
from {{ref('staging_violations')}}
where street_name is not null
group by
    dataset_year,street_name,house_number
order by count(summons_number) desc