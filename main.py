from typing import List

# FastAPI и зависимости
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
import uvicorn

# SQLAlchemy и база данных
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Boolean
from database import get_db, engine, Base # Модули проекта


# SQLAlchemy модель - БД
class task_model(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    complet = Column(Boolean, default=False)

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

class task_create(BaseModel):
    """Схема для создания задачи"""
    title: str
    description: str | None = None
    complet: bool = False

class task_response(BaseModel):
    """Схема для ответa"""
    id: int
    title: str
    description: str | None = None
    complet: bool = False
    model_config = {"from_attributes": True}


# Создаем экземпляр FastAPI
app = FastAPI(title="Task Manager")

# Эндпоинт для создания задачи
@app.post("/tasks/", tags=["Управление задачами"], response_model=task_response,
          summary="Создать задачу",description="Создает новую задачу в системе",
          response_description="Созданная задача")
def create_task(task: task_create, db: Session = Depends(get_db)):
    ex_task = db.query(task_model).filter(task_model.title == task.title).first()
    if ex_task: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Задача с таким названием уже существует")
    db_task = task_model(**task.model_dump())
    db.add(db_task)      # Для создания объекта БД
    db.commit()
    db.refresh(db_task)  # Для получения ID из БД
    return db_task


# Эндпоинт для просмотра задач
@app.get("/tasks/", tags=["Управление задачами"], response_model=List[task_response],
         summary="Получить список задач",description="Возвращает список всех задач",
         response_description="Список задач")
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(task_model).offset(skip).limit(limit).all() # Запрос к БД
    return tasks


# Эндпоинт для просмотра конкретной задачи
@app.get("/tasks/{task_id}",tags=["Управление задачами"], response_model=task_response,
         summary="Получить задачу по ID", description="Возвращает задачу по указанному идентификатору",
         response_description="Найденная задача")
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(task_model).filter(task_model.id == task_id).first() # Запрос к БД c поиском конкретной задачи
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


# Эндпоинт для обновления задачи
@app.put("/tasks/{task_id}",tags=["Управление задачами"],
         response_model=task_response, summary="Обновить задачу",
         description="Обновляет данные задачи по указанному ID",
         response_description="Обновленная задача")
def update_task(task_id: int, task_update: task_create, db: Session = Depends(get_db)):  # ← Принимаем схему без ID
    db_task = db.query(task_model).filter(task_model.id == task_id).first() # Поиск задачи в БД
    if not db_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    if db_task.complet == True:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя изменять завершенную задачу")
    update_data = task_update.model_dump(exclude_unset=True) # Передача только переданных полей
    for field, value in update_data.items(): # Процесс обновления полей
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task) # Обновление БД
    return db_task


# Эндпоинт для удаления задачи
@app.delete("/tasks/{task_id}", tags=["Управление задачами"], summary="Удалить задачу",
            description="Удаляет задачу по указанному идентификатору",
            response_description="Результат удаления")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(task_model).filter(task_model.id == task_id).first() # Поиск задачи
    if not db_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    db.delete(db_task) # Удаление
    db.commit()
    return {"message": "Задача успешно удалена"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)