from jupyter_plugin.plugin import JupyterDAG
from airflow.models import Variable
import datetime


# ------------------------------------------------------------------------
# Definição da DAG
# ------------------------------------------------------------------------
with JupyterDAG(
    'test_dag',
    jupyter_url=Variable.get('jupyter_url'),
    jupyter_token=Variable.get('jupyter_token'),
    jupyter_base_path=Variable.get('jupyter_base_path'),
    max_active_runs=1,
    default_args={
        'owner': 'Marcelo Vinicius',
        'depends_on_past': False,
        'start_date': datetime.datetime(2021, 1, 1),
        'email_on_failure': False,
        'email_on_retry': False,
        'retry_delay': datetime.timedelta(seconds=2),
        'retries': 1
    },
    description=f'DAG test to run some jupyter remote notebook.',
    schedule="@daily",
    catchup=False
) as dag:

    test1 = dag.create_jupyter_remote_operator(task_id="test1", notebook_path=f"notebooks/test1.ipynb")
    test2 = dag.create_jupyter_remote_operator(task_id="test2", notebook_path=f"notebooks/test2.ipynb")
    test3 = dag.create_jupyter_remote_operator(task_id="test3", notebook_path=f"notebooks/test3.ipynb")

test1 >> test2 >> test3

