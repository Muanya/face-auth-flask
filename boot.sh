#!/bin/sh
source venv/bin/activate
python manage.py db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - app:app
