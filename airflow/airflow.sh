#!/usr/bin/env sh

# Create ADMIN user
airflow users create \
    -u ${AIRFLOW_LOGIN} \
    -f apache \
    -l airflow \
    -r Admin \
    -e test@test.com \
    -p ${AIRFLOW_PASSWORD}

# Create airflow variables
airflow variables set jupyter_url "http://jupyter:8888"
airflow variables set jupyter_token "123"
airflow variables set jupyter_base_path "/home/jovyan/work"

# Install plugin manually
pip install build

# Check if plugin is installed
airflow plugin 