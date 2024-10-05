from airflow.plugins_manager import AirflowPlugin
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowException
from jupyter_plugin.jupyter_api_client import JupyterClient


class JupyterDAG(DAG):
    """
    This class extends the base DAG class in Airflow and simplifies the creation of tasks that execute Jupyter Notebooks. 
    It accepts Jupyter-specific parameters such as the URL, token, and notebook paths, which are used to set up the 
    connection to the remote Jupyter server.

    Args:
        DAG: Overwrites DAG class
    """

    def __init__(self, *args, **kwargs):
        self.jupyter_url = kwargs.pop("jupyter_url")
        self.jupyter_token = kwargs.pop("jupyter_token")
        self.jupyter_base_path = kwargs.pop("jupyter_base_path")
        super().__init__(*args, **kwargs)

    def create_jupyter_remote_operator(self, task_id, notebook_path):
        return JupyterRemoteNotebookOperator(
            task_id=task_id,
            jupyter_url=self.jupyter_url,
            jupyter_token=self.jupyter_token,
            jupyter_base_path=self.jupyter_base_path,
            notebook_path=notebook_path
        )


class JupyterRemoteNotebookOperator(PythonOperator):
    """
    A custom operator that inherits from PythonOperator and is used to run Jupyter Notebooks remotely. 
    It takes as input the Jupyter server's URL, token, and the path to the notebook that should be executed.

    Args:
        PythonOperator: Overwrites PythonOperator
    """

    def __init__(self, *args, **kwargs):
        self.jupyter_url = kwargs.pop('jupyter_url')
        self.jupyter_token = kwargs.pop('jupyter_token')
        self.jupyter_base_path = kwargs.pop('jupyter_base_path')
        self.jupyter_notebook_path = f"{self.jupyter_base_path}/{kwargs.pop('notebook_path')}"

        super().__init__(
            python_callable=self.execute,
            op_args=[self.jupyter_url, self.jupyter_token, self.jupyter_base_path, self.jupyter_notebook_path],
            *args,
            **kwargs
        )

    def execute(self, context):
        jupyter_api = JupyterClient(
            jupyter_token=self.jupyter_token,
            jupyter_url=self.jupyter_url,
            jupyter_notebook_path=self.jupyter_notebook_path
        )
        kernel_id = None

        try:
            params = context['params']
            kernel_id = jupyter_api.start_kernel()
            jupyter_api.start_session(kernel_id, self.jupyter_notebook_path)
            jupyter_api.run_notebook_code(kernel_id, params)
        except (AirflowException, KeyboardInterrupt) as e:
            raise RuntimeError(f"Error or iterruption: {str(e)}") from e
        finally:
            if kernel_id:
                jupyter_api.delete_kernel(kernel_id)
        return kernel_id


class JupyterPlugin(AirflowPlugin):
    """
    This is the Airflow plugin that ties everything together. 
    It registers the custom operator (JupyterRemoteNotebookOperator) and 
    the DAG processor (JupyterDAG) with Airflow, enabling their use in any DAG.

    Args:
        AirflowPlugin: Overwrites AirflowPlugin
    """
    name = "jupyter_plugin"
    operators = [JupyterRemoteNotebookOperator]
    dag_processors = [JupyterDAG]
