from sqlalchemy import Column, Integer, String, Boolean
from database import Base # Для импорта базового класса

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    complet = Column(Boolean, default=False)