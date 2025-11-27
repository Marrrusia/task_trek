from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import Task
from schemas import TaskCreate


class TaskCRUD:
    @staticmethod
    def get_task(db: Session, task_id: int):
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def get_tasks(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Task).offset(skip).limit(limit).all()

    @staticmethod
    def get_task_by_title(db: Session, title: str):
        return db.query(Task).filter(Task.title == title).first()

    @staticmethod
    def create_task(db: Session, task: TaskCreate):
        db_task = Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def update_task(db: Session, task_id: int, task_update: TaskCreate):
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            return None

        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: int):
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            return False

        db.delete(db_task)
        db.commit()
        return True