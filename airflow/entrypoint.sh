#!/usr/bin/env bash

# Verifica e remove o arquivo airflow-webserver.pid obsoleto (stale)
if [ -f "$AIRFLOW_HOME/airflow-webserver.pid" ]; then
  if ! ps -p $(cat "$AIRFLOW_HOME/airflow-webserver.pid") > /dev/null; then
    echo "Remove PID antigo..."
    rm "$AIRFLOW_HOME/airflow-webserver.pid"
  fi
fi

case "$1" in
  local)
    airflow db migrate      
    ./airflow.sh
    airflow webserver &     
    airflow scheduler      
    ;;
  webserver)
    airflow db migrate
    ./airflow.sh
    airflow webserver
    ;;
  worker)
    airflow celery worker
    ;;
  flower)
    airflow celery flower
    ;;
  scheduler|version)
    exec airflow "$@"
    ;;
  *)
    # Executa qualquer outro comando fornecido    
    exec "$@"
    ;;
esac