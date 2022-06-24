# Utility_MicroS
Usage : Micro Service for Utility functions
\
\
**Editor Used**         : VS Code
\
**Syntax Formatter**    : Black
\
\
Steps (Direct):
```
python -m install -r requirements.txt
python manage.py makemigrations api utilities
python manage.py migrate
```
\
\
Steps (Docker):
```
docker-compose up --remove-orphans
```
\
\
![ER](/utility/data/Schema-ER.jpg)\
![SCHEMA](/utility/data/Schema-URL.jpg)
\
\
[Postman Import](/utility/data/Utilities_MS.postman_collection.json)