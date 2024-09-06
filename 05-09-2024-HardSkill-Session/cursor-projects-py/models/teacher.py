from sqlalchemy import Column, Integer, String
from data.database import Base


class Teacher(Base):
    """Represents a teacher in the primary school."""

    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    subject = Column(String)
    teacher_id = Column(String, unique=True)

    def __str__(self):
        """Returns a string representation of the Teacher object."""
        return f"Teacher(name={self.name}, subject={self.subject}, teacher_id={self.teacher_id})"