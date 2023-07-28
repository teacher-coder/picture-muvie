#!/bin/sh

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
gunicorn picture_muvie.wsgi -w 3 -b 0.0.0.0:8000