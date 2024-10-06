# Airflow run Jupyter Notebook Remote 

- [Airflow run Jupyter Notebook Remote](#airflow-run-jupyter-notebook-remote)
  - [What is it?](#what-is-it)
  - [Would you mind buying me a coffee?](#would-you-mind-buying-me-a-coffee)
  - [Installation](#installation)
    - [Via Pypi Package:](#via-pypi-package)
    - [Manually](#manually)
  - [Airfow plugin dependencies](#airfow-plugin-dependencies)
  - [Test dependences](#test-dependences)
  - [How to contribute](#how-to-contribute)
  - [Credits](#credits)
  - [Run remote jupyter notebook using Airflow](#run-remote-jupyter-notebook-using-airflow)
  - [Plugin Usage](#plugin-usage)
  - [Run tests](#run-tests)

## What is it?

!['architecture'](https://raw.githubusercontent.com/marcelo225/airflow-remote-jupyter-notebook/main/architecture.png)

This plugin is designed to allow the execution of Jupyter Notebooks remotely from within an Airflow DAG. By using the plugin, users can integrate and manage Jupyter Notebook workflows as part of their Airflow pipelines, ensuring that data analysis or machine learning code can be orchestrated and run automatically within the DAG scheduling system.

The plugin utilizes the Jupyter API to communicate with a Jupyter server, allowing for operations such as starting a kernel, running notebook cells, and managing sessions. It supports both HTTP requests for session and kernel management and WebSocket connections for sending code to execute inside the notebooks.

Package link: https://pypi.org/project/airflow-remote-jupyter-notebook/

## Would you mind buying me a coffee?

If you find this library helpful, consider buying me a coffee! Your support helps maintain and improve the project, allowing me to dedicate more time to developing new features, fixing bugs, and providing updates.

![coffee](https://raw.githubusercontent.com/marcelo225/airflow-remote-jupyter-notebook/main/qr_code.png)

## Installation

### Via Pypi Package:

```bash
$ pip install airflow-remote-jupyter-notebook
```

### Manually

```bash
# run docker-compose to up Airfow and Jupyter Notebook containers
$ docker-compose up
```

## Airfow plugin dependencies

- Look at [requirements.txt](airflow/requirements.txt)

## Test dependences

- [pytest](https://docs.pytest.org)

## How to contribute

Please report bugs and feature requests at
https://github.com/marcelo225/airflow-remote-jupyter-notebook/issues

## Credits

Lead Developer - Marcelo Vinicius

## Run remote jupyter notebook using Airflow

```bash
# in root project folder
$ docker-compose up
```

- Open [http://localhost:8080](http://localhost:8080) in your web browser to open Airflow
- Open [http://localhost:8888](http://localhost:8888) in your web browser to open Jupyter Notebook, when you need it
- Run `test_dag` in Airflow

## Plugin Usage

```python

from jupyter_plugin.plugin import JupyterDAG # <--------- How to import this plugin
from airflow.models import Variable
import datetime

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
        'retries': 2        
    },
    description=f'DAG test to run some remote Jupyter Notebook file.',
    schedule=2,
    catchup=False
) as dag:

    test1 = dag.create_jupyter_remote_operator(task_id="test1", notebook_path=f"notebooks/test1.ipynb")
    test2 = dag.create_jupyter_remote_operator(task_id="test2", notebook_path=f"notebooks/test2.ipynb")
    test3 = dag.create_jupyter_remote_operator(task_id="test3", notebook_path=f"notebooks/test3.ipynb")

test1 >> test2 >> test3
```

| **DAG Attributes**    | **Description**                                                                 |
|-----------------------|---------------------------------------------------------------------------------|
| `jupyter_url`         | Jupyter URL server with HTTP or HTTPS                                           |
| `jupyter_token`       | Jupyter Authentication Token                                                    |
| `jupyter_base_path`   | Base path where your Jupyter notebooks are stored                               |


| **Task Creation**     | **Explanation**                                                                 |
|-----------------------|---------------------------------------------------------------------------------|
| `create_jupyter_remote_operator` | Method from the `JupyterDAG` class that creates a task to execute a specified Jupyter notebook on a remote server. |
| `task_id`              | A unique identifier for the task, used for tracking and logging within Airflow.  |
| `notebook_path`        | Specifies the path to the Jupyter notebook to be executed, relative to the base path. |


## Run tests

To test the scripts within the Airflow environment, you can use the following command. 
This will run all tests located in the **/home/airflow/tests** directory inside the container:

```bash
$ docker-compose exec airflow pytest /home/airflow/tests
```