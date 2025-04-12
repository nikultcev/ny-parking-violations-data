from airflow import DAG
from airflow.operators.bash import BashOperator

default_command = 'cd $AIRFLOW_HOME/plugins/dbt && dbt run --select'

with DAG(
    dag_id='run_dbt_models',
    schedule=None,
    catchup=False,
) as dag:

    staging_violations = BashOperator(
        task_id='staging_violations',
        bash_command=f'{default_command} staging_violations'
    )

    parking_violation_codes = BashOperator(
        task_id='parking_violation_codes',
        bash_command='cd $AIRFLOW_HOME/plugins/dbt && dbt seed'
    )

    violations_by_code = BashOperator(
        task_id='violations_by_code',
        bash_command=f'{default_command} violations_by_code'
    )

    violations_by_fiscal_year = BashOperator(
        task_id='violations_by_fiscal_year',
        bash_command=f'{default_command} violations_by_fiscal_year'
    )

    violations_by_street = BashOperator(
        task_id='violations_by_street',
        bash_command=f'{default_command} violations_by_street'
    )


    staging_violations>>parking_violation_codes>>[violations_by_code,violations_by_fiscal_year,violations_by_street]