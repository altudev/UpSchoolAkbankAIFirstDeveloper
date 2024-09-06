from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from data.database import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="lessons")