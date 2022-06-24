FROM python:3.11.0b3-alpine3.16
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app
# RUN apk add --no-cache libxml2 libxslt
RUN pip install -r requirements.txt

WORKDIR /app/utility
RUN python manage.py makemigrations api utilities
RUN python manage.py migrate

CMD ["python manage.py runserver","0.0.0.0:8000"]