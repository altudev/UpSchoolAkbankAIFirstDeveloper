from pydantic import BaseModel
from datetime import date

class TodoCreate(BaseModel):
    text: str
    completed: bool = False
    deadline: date

class Todo(TodoCreate):
    id: int

    class Config:
        orm_mode = True