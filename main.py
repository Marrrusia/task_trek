from typing import List
#Для работы с fastapi
from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
#Для работы с бд
from sqlalchemy.orm import Session
#Импорты локальных модулей
from database import get_db, engine
from models import Task
from schemas import TaskCreate, TaskResponse
from crud import TaskCRUD

# Создание таблиц в базе данных
Task.metadata.create_all(bind=engine)

# Создаем экземпляр FastAPI
app = FastAPI(title="Task Manager")


# Эндпоинт для создания задачи
@app.post("/tasks/",tags=["Управление задачами"], response_model=TaskResponse, summary="Создать задачу",
          description="Создает новую задачу в системе",response_description="Созданная задача")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    existing_task = TaskCRUD.get_task_by_title(db, task.title) # Существует ли задача с таким названием
    if existing_task: raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,
            detail="Задача с таким названием уже существует")
    return TaskCRUD.create_task(db, task)  # создание задачи


# Эндпоинт для просмотра задач
@app.get("/tasks/",tags=["Управление задачами"],response_model=List[TaskResponse],
         summary="Получить список задач",description="Возвращает список всех задач",
         response_description="Список задач")
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return TaskCRUD.get_tasks(db, skip, limit)


# Эндпоинт для просмотра конкретной задачи
@app.get("/tasks/{task_id}",tags=["Управление задачами"],response_model=TaskResponse,
         summary="Получить задачу по ID", description="Возвращает задачу по указанному идентификатору",
         response_description="Найденная задача")
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = TaskCRUD.get_task(db, task_id) # Поиск и возврат задачи
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


# Эндпоинт для обновления задачи
@app.put("/tasks/{task_id}", tags=["Управление задачами"], response_model=TaskResponse,
         summary="Обновить задачу", description="Обновляет данные задачи по указанному ID",
         response_description="Обновленная задача")
def update_task(task_id: int, task_update: TaskCreate, db: Session = Depends(get_db)):
    db_task = TaskCRUD.get_task(db, task_id) # Проверяем существование задачи
    if not db_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    if db_task.complet:  # Проверяем, не завершена ли задача
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя изменять завершенную задачу"  )
    updated_task = TaskCRUD.update_task(db, task_id, task_update) #обновление задачи
    return updated_task


# Эндпоинт для удаления задачи
@app.delete("/tasks/{task_id}", tags=["Управление задачами"], summary="Удалить задачу",
            description="Удаляет задачу по указанному идентификатору",
            response_description="Результат удаления")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = TaskCRUD.delete_task(db, task_id) #elfktybt pflfxb
    if not success:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"message": "Задача успешно удалена"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)