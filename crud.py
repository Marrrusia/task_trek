#Для работы с бд
from sqlalchemy.orm import Session
#Импорты локальных модулей
from models import Task
from schemas import TaskCreate


class TaskCRUD:
    @staticmethod # Получение задачи по ее ID
    def get_task(db: Session, task_id: int):
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod # Получение списка задач
    def get_tasks(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Task).offset(skip).limit(limit).all()

    @staticmethod # Поиск задачи в БД, используется для предотвращения дублирования
    def get_task_by_title(db: Session, title: str):
        return db.query(Task).filter(Task.title == title).first()

    @staticmethod #Создание задачи
    def create_task(db: Session, task: TaskCreate):
        db_task = Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task) # Для получения ID задачи
        return db_task

    @staticmethod #Обновление задачи
    def update_task(db: Session, task_id: int, task_update: TaskCreate):
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            return None
        update_data = task_update.model_dump(exclude_unset=True) #Для обновления только переданных полей
        for field, value in update_data.items():
            setattr(db_task, field, value)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod # Удаление задачи по ее ID
    def delete_task(db: Session, task_id: int):
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task: #Проверка на наличие задачи
            return False
        db.delete(db_task)
        db.commit()
        return True