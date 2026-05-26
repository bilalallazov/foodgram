#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
for i in $(seq 1 30); do
  if python -c "
import os
import psycopg2
psycopg2.connect(
    dbname=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host=os.environ.get('DB_HOST', 'db'),
    port=os.environ.get('DB_PORT', '5432'),
).close()
"; then
    break
  fi
  sleep 2
done

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py load_ingredients
python manage.py create_tags
python manage.py load_test_data

exec gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
