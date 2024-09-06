from sqlalchemy import Column, Integer, String
from data.database import Base


class Student(Base):
    """Represents a student in the primary school."""

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    grade = Column(Integer)
    student_id = Column(String, unique=True)

    def __str__(self):
        """Returns a string representation of the Student object."""
        return f"Student(name={self.name}, grade={self.grade}, student_id={self.student_id})"

