with yearly_stats as (
    select
        dataset_year,
        count(summons_number) as count
    from {{ref('staging_violations')}}
    group by
        dataset_year
)
select
    dataset_year as fiscal_year,
    count as violations,
    (count-lag(count) over (order by dataset_year))/count as yoy_change
from yearly_stats
order by dataset_year