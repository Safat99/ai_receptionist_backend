#!/bin/bash
source venv/bin/activate
flask db upgrade
flask translate compile

# gunicorn -b :5000 --access-logfile - --error-logfile - manage:app
python manage.py run -h 0.0.0.0