#!/usr/bin/env bash
until pg_isready -h "${DB_HOST}" -p 5432 -U "${DB_USER}":"${DB_PASSWORD}" -d "${DB_NAME}"
do
  echo "Waiting for postgres 5 sec ... "
  sleep 5;
done

echo "Creating missing migrations"
python manage.py makemigrations

echo "Migrating..."
python manage.py migrate

if [ "$?" = "1" ]; then
  echo "Failed to run migration"
  exit 1
fi

echo "Running server"
python manage.py runserver 0.0.0.0:8000
