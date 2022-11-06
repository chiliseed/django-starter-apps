FROM python:3.11.0-slim-buster AS base

LABEL maintainer="Chiliseed LTD"

ARG requirements=requirements/dev.txt
ENV PATH=$PATH:/app
ENV PYTHONPATH=$PYTHONPATH:/app

RUN mkdir /app
WORKDIR /app

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
        gcc \
        libpq-dev \
        postgresql-client && \
        apt-get clean

COPY requirements requirements

RUN pip install -r ${requirements}

COPY src/ /app


FROM base AS prod

RUN mkdir -p /app/statics

CMD python manage.py collectstatic --noinput && python manage.py migrate && gunicorn -w 3 --bind 0.0.0.0:8000 --timeout 90 backend.wsgi
