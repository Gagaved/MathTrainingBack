from pydantic import BaseModel

class ExerciseBase(BaseModel):
    title: str
    body: str

class ExerciseCreate(ExerciseBase):
    pass

class Exercise(ExerciseBase):
    id: int

    class Config:
        orm_mode = True
