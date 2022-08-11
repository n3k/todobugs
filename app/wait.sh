#!/usr/bin/env sh

while ! nc -z db 3306 ; do
    echo "Waiting for the MySQL Server"
    sleep 3
done

python ./todobugs/manage.py migrate

echo "$(pwd)"
python ./todobugs/manage.py runserver 0.0.0.0:8000

#gunicorn todobugs.wsgi -b 0:8000