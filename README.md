**Task Manager API**

Простое API для управления задачами на FastAPI.

**Для запуска с докером введите**

docker-compose up --build

Можно запуститить без докера

pip install -r requirements.txt

python main.py

**Документация**
После запуска откройте http://localhost:8000/docs для просмотра документации API.

**Доступные методы**
- GET /tasks/ - список задач
- POST /tasks/ - создать задачу
- GET /tasks/{id} - получить задачу
- PUT /tasks/{id} - обновить задачу
- DELETE /tasks/{id} - удалить задачу
