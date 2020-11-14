# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.134.1/containers/alpine/.devcontainer/base.Dockerfile
ARG PYTHON_VERSION="3.8"
FROM python:${PYTHON_VERSION}-buster as base-python

# https://pythonspeed.com/articles/multi-stage-docker-python/
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN python -m pip install --upgrade pip
# For faster instalation
RUN pip install wheel
RUN pip install --no-cache-dir --no-warn-script-location pandas numpy jupyter requests matplotlib dash beautifulsoup4 googlemaps



# Copy installed python
COPY --from=base-python /opt/venv /opt/venv
COPY --from=base-python /usr/local/bin /usr/local/bin
COPY --from=base-python /usr/local/lib /usr/local/lib
ENV LD_LIBRARY_PATH='/lib:/usr/lib:/usr/local/lib'

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# This enables us to install additional python libraries
USER root
# Expose jupyter port
EXPOSE 8888