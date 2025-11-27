from pydantic import BaseModel


class TaskCreate(BaseModel):
    """Схема для создания задачи"""
    title: str
    description: str | None = None
    complet: bool = False


class TaskResponse(BaseModel):
    """Схема для ответа"""
    id: int
    title: str
    description: str | None = None
    complet: bool = False

    model_config = {"from_attributes": True}