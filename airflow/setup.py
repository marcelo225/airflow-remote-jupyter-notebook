from setuptools import setup, find_packages

setup(
    name="jupyter_plugin",
    version="0.0.1",
    description="Airflow plugin to execute Jupyter Notebook remotely",
    author="Marcelo Vinicius",
    author_email="mr.225@hotmail.com",
    packages=find_packages(where='plugins'),
    entry_points={
        'airflow.plugins': [
            'jupyter_plugin = jupyter_plugin.plugin:JupyterDAG'
        ]
    },
    install_requires=[
        'requests',
        'websockets',
        'asyncio'
    ],
)