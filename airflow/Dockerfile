FROM python:3.10.1-slim-buster

USER root

# variables is for building your Docker image
ARG UID=1000
ARG GID=1000
ARG UNAME=airflow
ARG GNAME=airflow
ARG HOME_PATH=/home

# variables is for future running containers
ENV AIRFLOW_HOME=${HOME_PATH}/airflow
ENV AIRFLOW_LOG_FOLDER=${AIRFLOW_HOME}/logs
ENV AIRFLOW_PLUGIN_FOLDER=${AIRFLOW_HOME}/plugins

# update python and global env paths
ENV PYTHONPATH=${AIRFLOW_HOME}

# Add pip user folder to PATH to avoid pip installing errors
ENV PATH="${HOME_PATH}/.local/bin:${PATH}"

# Create airflow project folder and pip folder
RUN mkdir ${AIRFLOW_HOME}

# Set user permissions at aiflow folder
RUN groupadd -g ${GID} ${UNAME}
RUN useradd -u ${UID} -m -d ${HOME_PATH} -g ${GID} ${UNAME}
RUN chown -R ${UNAME}:${GNAME} ${HOME_PATH}

# Copy app files
COPY --chown=${UNAME}:${GNAME} entrypoint.sh ${AIRFLOW_HOME}
COPY --chown=${UNAME}:${GNAME} requirements.txt ${AIRFLOW_HOME}
COPY --chown=${UNAME}:${GNAME} airflow.sh ${AIRFLOW_HOME}
COPY --chown=${UNAME}:${GNAME} logs/ ${AIRFLOW_LOG_FOLDER}
COPY --chown=${UNAME}:${GNAME} plugins/ ${AIRFLOW_PLUGIN_FOLDER}

# Change access permissions
RUN chmod -R 777 /tmp
RUN chmod -R 777 ${AIRFLOW_LOG_FOLDER}
RUN chmod +x ${AIRFLOW_HOME}/entrypoint.sh

# Update pip
RUN pip3 install --no-cache-dir --upgrade pip

# Install other python dependencies
RUN pip3 install -r ${AIRFLOW_HOME}/requirements.txt

# Define user home
USER ${UNAME}

WORKDIR $AIRFLOW_HOME

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
CMD ["--help"]
