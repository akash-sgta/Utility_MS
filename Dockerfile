FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
# RUN python manage.py makemigrations api utilities
# RUN python manage.py migrate

CMD python manage.py runserver 0.0.0.0:8000