select 
    initcap(codes.description) as violation_name,
    count(summons_number) as violations,
    round(count(summons_number)/sum(count(summons_number)) OVER (),2) as violations_share_of_total
from {{ref('staging_violations')}} as violations
    left outer join {{ref('parking_violation_codes')}} as codes on 
        codes.id = violations.violation_code
where nullif(codes.description,'') is not null
group by
    initcap(codes.description)
order by count(summons_number) desc