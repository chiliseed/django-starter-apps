#!/bin/sh
sleep 10

until pg_isready -h ${DB_HOST} -p 5432 -U ${DB_USER}:${DB_PASSWORD} -d ${DB_NAME}
do
  echo "Waiting for postgres 5 sec ... "
  sleep 5;
done

# Django check
python manage.py check

# Start celery worker via watchdog
# Start with beat scheduler as well; ok in development, not in production!
celery -A demo worker -l info
