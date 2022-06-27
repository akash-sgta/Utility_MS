# Utility_MicroS
Usage : Micro Service for Utility functions  
___
**Editor Used**         : VS Code  
**Syntax Formatter**    : Black
___
Steps (Direct):
```
python -m install -r requirements.txt
python manage.py makemigrations api utilities
python manage.py migrate
```
Steps (Docker):
```
docker system prune
docker-compose up
docker-compose exec backend sh
```
___
**Drawio Save**  
[Schema.xml](/utility/data/Schema.xml)  
**Postman Import**  
[Utilities_MS.postman_collection.json](/utility/data/Utilities_MS.postman_collection.json)  
___