#!/bin/bash
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py load_ingredients
python manage.py create_tags
python manage.py load_test_data

exec gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
