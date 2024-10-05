FROM python:3.10.1-slim-buster

USER root

# Variables for building the Docker image
ARG UID=1000
ARG GID=1000
ARG UNAME=airflow
ARG GNAME=airflow
ARG HOME_PATH=/home

# Variables for future running containers
ENV AIRFLOW_HOME=${HOME_PATH}/airflow
ENV AIRFLOW_LOG_FOLDER=${AIRFLOW_HOME}/logs
ENV AIRFLOW_PLUGIN_FOLDER=${AIRFLOW_HOME}/plugins

# Update Python and global environment paths
ENV PYTHONPATH=${AIRFLOW_HOME}

# Add pip user folder to PATH to avoid pip installation errors
ENV PATH="${HOME_PATH}/.local/bin:${PATH}"

# Create airflow project folder and pip cache folder
RUN mkdir -p ${AIRFLOW_HOME} ${HOME_PATH}/.local ${HOME_PATH}/.cache/pip

# Create pytest cache directory and adjust permissions
RUN mkdir -p ${HOME_PATH}/.pytest_cache && \
    chown -R ${UNAME}:${GNAME} ${HOME_PATH}/.pytest_cache && \
    chmod -R 777 ${HOME_PATH}/.pytest_cache

# Set user permissions for the airflow folder and create airflow user
RUN groupadd -g ${GID} ${UNAME} && \
    useradd -u ${UID} -m -d ${HOME_PATH} -g ${GID} ${UNAME} && \
    chown -R ${UNAME}:${GNAME} ${HOME_PATH}

# Copy application files
COPY --chown=${UNAME}:${GNAME} entrypoint.sh ${AIRFLOW_HOME}
COPY --chown=${UNAME}:${GNAME} requirements.txt ${AIRFLOW_HOME}
COPY --chown=${UNAME}:${GNAME} airflow.sh ${AIRFLOW_HOME}
COPY --chown=${UNAME}:${GNAME} logs/ ${AIRFLOW_LOG_FOLDER}
COPY --chown=${UNAME}:${GNAME} plugins/ ${AIRFLOW_PLUGIN_FOLDER}

# Create and adjust permissions for the scheduler logs directory
RUN chown -R ${UNAME}:${GNAME} ${AIRFLOW_LOG_FOLDER} && \
    chmod -R 777 ${AIRFLOW_LOG_FOLDER}

# Adjust permissions for /tmp and make entrypoint executable
RUN chmod +x ${AIRFLOW_HOME}/entrypoint.sh

# Upgrade pip globally
RUN pip3 install --no-cache-dir --upgrade pip

# Install other Python dependencies globally
RUN pip3 install --no-cache-dir -r ${AIRFLOW_HOME}/requirements.txt

# Ensure the airflow user has write access to pip cache folders
RUN chown -R ${UNAME}:${GNAME} ${HOME_PATH}/.local ${HOME_PATH}/.cache/pip

# Define user home and switch to airflow user
USER ${UNAME}
WORKDIR $AIRFLOW_HOME

# Expose the airflow webserver port
EXPOSE 8080

# Set entrypoint
ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
CMD ["--help"]
