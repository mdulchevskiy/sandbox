FROM python:3.11.4-slim

# Do not buffer output
ENV PYTHONUNBUFFERED 1

# Do not write pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Create a group and user to run app
ARG APP_USER=appuser
ARG MAC_HOST_UID=501
ARG LINUX_HOST_UID=1000
RUN groupadd -r ${APP_USER} && useradd --no-log-init --create-home -r -u ${MAC_HOST_UID} -g ${APP_USER} ${APP_USER}

RUN chmod 1777 /tmp
RUN chmod 777 /opt /run

# Create project directory
ARG APP_DIR=/code
RUN mkdir ${APP_DIR} && chown ${APP_USER}:${APP_USER} ${APP_DIR}

# Install packages needed to run application (not build deps):
#
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -eux pipefail \
    && RUN_DEPS=" \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt ${APP_DIR}/requirements.txt

# Install build deps, then run `pip install` and others commands,
# then remove unneeded build deps all in a single step.
RUN set -eux pipefail \
    && BUILD_DEPS=" \
    git \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --upgrade pip && pip install --no-cache-dir -r ${APP_DIR}/requirements.txt \
    && git clone https://github.com/vishnubob/wait-for-it.git \
    && cd wait-for-it / \
    && cp ./wait-for-it.sh / \
    && chmod +x /wait-for-it.sh \
    && rm -rf /wait-for-it \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR ${APP_DIR}

# Copy application code to the container
ADD . ${APP_DIR}

# Change to a non-root user
USER ${APP_USER}:${APP_USER}
