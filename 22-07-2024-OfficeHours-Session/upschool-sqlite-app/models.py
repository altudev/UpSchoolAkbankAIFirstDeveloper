from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cat(Base):
    __tablename__ = 'cats'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    breed = Column(String(50))
    age = Column(Integer)
    colour = Column(String(20))

    def __repr__(self):
        return f"<Cat(id='{self.id}' ,name='{self.name}', breed='{self.breed}', age={self.age}, colour='{self.colour}')>"