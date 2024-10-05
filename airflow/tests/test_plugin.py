import pytest
from unittest.mock import patch
from plugins.jupyter_plugin.plugin import JupyterDAG, JupyterRemoteNotebookOperator
from airflow.models import Variable
from config import JUPYTER_URL, JUPYTER_TOKEN, JUPYTER_NOTEBOOK_PATH
import datetime


# Mock das variáveis do Airflow
@pytest.fixture(autouse=True)
def mock_variables():
    with patch.object(Variable, 'get') as mock_get:
        mock_get.side_effect = lambda var_name: {
            'jupyter_url': JUPYTER_URL,
            'jupyter_token': JUPYTER_TOKEN,
            'jupyter_base_path': JUPYTER_NOTEBOOK_PATH
        }.get(var_name)
        yield

# Teste para criação do JupyterDAG
def test_jupyter_dag_creation():
    dag = JupyterDAG(
        'test_dag',
        jupyter_url=Variable.get('jupyter_url'),
        jupyter_token=Variable.get('jupyter_token'),
        jupyter_base_path=Variable.get('jupyter_base_path'),
        max_active_runs=1,
        default_args={
            'owner': 'Marcelo Vinicius',
            'depends_on_past': False,
            'start_date': datetime.datetime(2021, 1, 1),
        },
        schedule="@daily",
        catchup=False
    )

    assert dag.jupyter_url == JUPYTER_URL
    assert dag.jupyter_token == JUPYTER_TOKEN
    assert dag.jupyter_base_path == JUPYTER_NOTEBOOK_PATH

# Teste para criação do operador remoto
def test_create_jupyter_remote_operator():
    dag = JupyterDAG(
        'test_dag',
        jupyter_url=Variable.get('jupyter_url'),
        jupyter_token=Variable.get('jupyter_token'),
        jupyter_base_path=Variable.get('jupyter_base_path'),
        max_active_runs=1,
        default_args={
            'owner': 'Marcelo Vinicius',
            'depends_on_past': False,
            'start_date': datetime.datetime(2021, 1, 1),
        },
        schedule="@daily",
        catchup=False
    )

    operator = dag.create_jupyter_remote_operator(
        task_id="test_task",
        notebook_path=JUPYTER_NOTEBOOK_PATH
    )

    assert isinstance(operator, JupyterRemoteNotebookOperator)
    assert operator.jupyter_url == JUPYTER_URL
    assert operator.jupyter_token == JUPYTER_TOKEN
