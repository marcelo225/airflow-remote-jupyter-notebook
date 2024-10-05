FROM python:3.10.1-slim-buster

USER root

# variables for building the Docker image
ARG UID=1000
ARG GID=1000
ARG UNAME=airflow
ARG GNAME=airflow
ARG HOME_PATH=/home

# variables for future running containers
ENV AIRFLOW_HOME=${HOME_PATH}/airflow
ENV AIRFLOW_LOG_FOLDER=${AIRFLOW_HOME}/logs
ENV AIRFLOW_PLUGIN_FOLDER=${AIRFLOW_HOME}/plugins

# update python and global env paths
ENV PYTHONPATH=${AIRFLOW_HOME}

# Add pip user folder to PATH to avoid pip installing errors
ENV PATH="${HOME_PATH}/.local/bin:${PATH}"

# Create airflow project folder and pip folder
RUN mkdir -p ${AIRFLOW_HOME} ${HOME_PATH}/.cache/pip

# Set user permissions for the airflow folder
RUN groupadd -g ${GID} ${UNAME} && \
    useradd -u ${UID} -m -d ${HOME_PATH} -g ${GID} ${UNAME} && \
    chown -R ${UNAME}:${GNAME} ${HOME_PATH}

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

# Update pip globally as root
RUN pip3 install --no-cache-dir --upgrade pip

# Ensure airflow user has write access to .local and .cache directories
RUN mkdir -p ${HOME_PATH}/.local && \
    mkdir -p ${HOME_PATH}/.cache/pip && \
    chown -R ${UNAME}:${GNAME} ${HOME_PATH}/.local ${HOME_PATH}/.cache/pip

# Switch to airflow user before installing packages
USER ${UNAME}

# Install Python dependencies as airflow user (avoids permission errors)
RUN pip3 install --no-cache-dir --user -r ${AIRFLOW_HOME}/requirements.txt

# Set airflow home as working directory
WORKDIR $AIRFLOW_HOME

# Expose the airflow web server port
EXPOSE 8080

# Set entrypoint
ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
CMD ["--help"]
