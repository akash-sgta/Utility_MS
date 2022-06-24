FROM python:3.8.13-alpine3.16
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app
RUN apk add --no-cache libxml2-dev
RUN apk add --no-cache libxslt-dev
RUN apk add --no-cache gcc
RUN apk add --no-cache musl-dev
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk add --no-cache build-base
RUN apk add --no-cache libressl-dev
RUN apk add --no-cache libffi-dev
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# WORKDIR /app/utility
# RUN python manage.py makemigrations api utilities
# RUN python manage.py migrate

CMD ["sh", "/app/run_me.sh"]