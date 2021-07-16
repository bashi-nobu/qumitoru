#!/bin/bash
sleep 5
python manage.py makemigrations --settings qumitoru.settings.prd
python manage.py migrate --settings qumitoru.settings.prd

python manage.py collectstatic --settings qumitoru.settings.prd
python manage.py collectstatic --noinput
# uwsgi --socket :8001 --module qumitoru.wsgi
