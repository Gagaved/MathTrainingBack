from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ExerciseUserProgression(Base):
    __tablename__ = "exercise_user_progression"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    task_id = Column(Integer)
    progression = Column(Integer)
