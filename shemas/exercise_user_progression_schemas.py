from pydantic import BaseModel

class ExerciseUserProgressionBase(BaseModel):
    user_id: int
    task_id: int
    progression: int

class ExerciseUserProgressionCreate(ExerciseUserProgressionBase):
    pass

class ExerciseUserProgression(ExerciseUserProgressionBase):
    id: int

    class Config:
        orm_mode = True
