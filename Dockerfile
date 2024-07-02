# SPDX-FileCopyrightText: 2024-present Stuart Ellis <stuart@stuartellis.name>
#
# SPDX-License-Identifier: CC0-1.0
#

ARG DOCKER_IMAGE_BASE=python:3.12-slim-bookworm
ARG PYTHON_REQS_FILE=requirements-app.in.txt

#============ BASE ===========

FROM ${DOCKER_IMAGE_BASE} as base_python

RUN apt-get update -q && \
    apt-get upgrade -qy

#========== BUILDER ==========

FROM base_python as builder

ARG PYTHON_REQS_FILE

ENV PIP_NO_CACHE_DIR=1 PIP_TIMEOUT=120
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1 PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get install --no-install-recommends -qy \
        curl build-essential

RUN python -m venv /opt/venv
COPY ./${PYTHON_REQS_FILE} ./
RUN . /opt/venv/bin/activate \
        && pip install --upgrade pip \
        && pip install -r ${PYTHON_REQS_FILE}

#=========== APP ============

FROM base_python as app

RUN rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 appusers \
  && useradd --uid 1000 --gid appusers --shell /bin/bash --create-home appuser

RUN mkdir /app && chown -R appuser:appusers /app

COPY --from=builder --chown=appuser:appusers /opt/venv /opt/venv
COPY --chown=appuser:appusers . /app

WORKDIR /app

USER appuser
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1 PYTHONUNBUFFERED=1

# FIXME: Currently a placeholder.
# The HEALTHCHECK, CMD and related settings depend on the application.
HEALTHCHECK NONE
CMD . /opt/venv/bin/activate && python3 -m tfg
