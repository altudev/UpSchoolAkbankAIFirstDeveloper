from sqlalchemy.orm import Session
from models import TodoDB
from schemas import TodoCreate

def create_todo(db: Session, todo: TodoCreate):
    db_todo = TodoDB(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TodoDB).offset(skip).limit(limit).all()

def get_todo(db: Session, todo_id: int):
    return db.query(TodoDB).filter(TodoDB.id == todo_id).first()

def update_todo(db: Session, todo_id: int, todo: TodoCreate):
    db_todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if db_todo:
        for key, value in todo.dict().items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return todo