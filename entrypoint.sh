#!/bin/bash

python3.9 manage.py makemigrations --no-input
python3.9 manage.py migrate --no-input
python3.9 manage.py collectstatic --no-input


exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --reload