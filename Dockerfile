FROM python:3.10.10-slim@sha256:582078f93e627c71de2279d0d8e58233bc2d626db03659ade3c01d68d325ed61

LABEL org.opencontainers.image.authors="Ken Shibata <+@nyiyui.ca>, Kyunghan (Paul) Lee <contact@paullee.dev>"
LABEL org.opencontainers.image.source="https://github.com/wlmac/metropolis"

RUN adduser --system --home /app --gecos "Metropolis" app && \
    groupadd app && \
    usermod -g app app && \
    apt-get update && \
    apt-get install -y build-essential python3-dev libpq-dev libffi-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app2/media
WORKDIR /app2/static
WORKDIR /app
USER app
RUN python -m pip install --no-cache-dir poetry

COPY poetry.lock pyproject.toml /app/
RUN python -m poetry config virtualenvs.in-project true && \
    python -m poetry install --no-root && \
    /app/.venv/bin/python3 -m pip install --no-cache-dir psycopg2
USER root
RUN apt-get purge -y build-essential python3-dev libpq-dev libffi-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/*
RUN rm -rf /var/cache/*
USER app

COPY . /app/
COPY ./metropolis/docker_settings.py /app/metropolis/local_settings.py

USER root
EXPOSE 28780
CMD /app/.venv/bin/gunicorn \
      --bind :28780 \
      --error-logfile - \
      --config /app/container/gunicorn.py \
      metropolis.wsgi:application
