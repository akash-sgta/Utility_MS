#!/bin/bash
sleep 10
python /app/utility/manage.py makemigrations api utilities && python /app/utility/manage.py migrate
python /app/utility/manage.py runserver 0.0.0.0:8000