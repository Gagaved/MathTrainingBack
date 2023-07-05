from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(Text)
