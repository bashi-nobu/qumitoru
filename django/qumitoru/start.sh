#!/bin/bash
sleep 5

if [ "$DJANGO_ENV" = "dev" ]; then
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createcustomsuperuser \
    --username admin --password 123456 --noinput --email email@example.com
    python3 manage.py runserver 0.0.0.0:8001
else
    python manage.py makemigrations --settings qumitoru.settings.prd
    python manage.py migrate --settings qumitoru.settings.prd

    python manage.py collectstatic --settings qumitoru.settings.prd
    python manage.py collectstatic --noinput
fi
