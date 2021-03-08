#!/bin/sh
sleep 10

until pg_isready -h "${DB_HOST}" -p 5432 -U "${DB_USER}:${DB_PASSWORD}" -d "${DB_NAME}"
do
  echo "Waiting for postgres 5 sec ... "
  sleep 5;
done

# Django check
python manage.py check

exec watchmedo auto-restart -d . -p "*.py" --recursive -- \
  dockerize -wait http://api:8000/health/check/ \
  celery -A backend worker -l info -B --concurrency 4

