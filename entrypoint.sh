#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# 環境変数のDEBUGの値によって開発環境か本番環境かを判定
if [ "$DEBUG" = "True" ]
then
    python manage.py runserver 0.0.0.0:8000
else
    # gunicornを起動
    gunicorn project.wsgi:application --bind 0.0.0.0:8000
fi