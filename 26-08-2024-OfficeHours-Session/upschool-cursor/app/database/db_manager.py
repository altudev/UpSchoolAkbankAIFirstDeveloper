from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import Config
from ..models.chat import Base

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()