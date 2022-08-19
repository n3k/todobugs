#!/usr/bin/env sh

while ! nc -z db 3306 ; do
    echo "Waiting for the MySQL Server"
    sleep 3
done


python ./todobugs/manage.py makemigrations myapp
python ./todobugs/manage.py makemigrations webadmin
python ./todobugs/manage.py migrate
#python ./todobugs/manage.py collectstatic

echo "from django.contrib.auth.models import User; User.objects.create_superuser('rick', 'rick@citadel.com', 'morty2022')" | python ./todobugs/manage.py shell


echo "$(pwd)"
#python ./todobugs/manage.py runserver 0.0.0.0:8000
export PYTHONPATH=./todobugs

gunicorn todobugs.wsgi -b 0:8000