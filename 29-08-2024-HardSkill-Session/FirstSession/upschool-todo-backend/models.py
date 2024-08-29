from sqlalchemy import Column, Integer, String, Boolean, Date
from database import Base

class TodoDB(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    completed = Column(Boolean, default=False)
    deadline = Column(Date)