**Task Manager API**

API для управления задачами на FastAPI.

**Доступные методы**
- GET /tasks/ - получить список задач
- POST /tasks/ - создать задачу
- GET /tasks/{id} - получить задачу
- PUT /tasks/{id} - обновить задачу
- DELETE /tasks/{id} - удалить задачу

**Инструкция**

Для запуска системы нам потребуется установленный Docker и Docker Compose.  
Команды для запуска:  
Запуск в фоновом режиме: docker-compose up -d  
Остановка системы: docker-compose down  

После запуска откройте http://localhost:8000/docs для просмотра документации API.

Выбирается эндпоинт:

Эндпоинты API

1. Создание задачи  
Метод: POST  
URL: /tasks/  
Вводится заголовок и описание задачи:  
<img width="895" height="478" alt="Снимок экрана 2025-11-30 в 18 00 25" src="https://github.com/user-attachments/assets/70599a89-cad3-4ff9-a03d-605488bd6e44" />

2. Получение списка задач     
Метод: GET  
URL: /tasks/  
Параметры запроса:  
skip - количество пропускаемых записей (по умолчанию: 0)  
limit - максимальное количество возвращаемых записей (по умолчанию: 10)  
Вводится какая задача выводятся первой и количество задач, которые выводятся:  
<img width="902" height="314" alt="Снимок экрана 2025-11-30 в 18 00 31" src="https://github.com/user-attachments/assets/85727014-c6c5-414e-a417-99b3ed49b087" />

3. Получение конкретной задачи  
Метод: GET  
URL: /tasks/{id}  
Вводится номер конкретной задачи для ее получения:  
<img width="905" height="263" alt="Снимок экрана 2025-11-30 в 18 00 36" src="https://github.com/user-attachments/assets/a7a18bbd-7a83-43b8-85bb-3bcdd2f1effc" />

4. Обновление задачи  
Метод: PUT  
URL: /tasks/{id}  
Вводится номер обновляемой задачи и параметры, которые мы хотим обновить:  
<img width="906" height="348" alt="Снимок экрана 2025-11-30 в 18 00 44" src="https://github.com/user-attachments/assets/e164e4e6-77d7-4827-9cb6-edebf37c6206" />

5. Удаление задачи  
Метод: DELETE  
URL: /tasks/{id}  
Вводится номер задачи для удаления в task_id:  
<img width="902" height="268" alt="Снимок экрана 2025-11-30 в 18 00 52" src="https://github.com/user-attachments/assets/9b8adc7c-fa2d-427a-bfcc-d02678ca4cc3" />

При возникновении ошибки система возвращает стандартные HTTP коды состояния.
