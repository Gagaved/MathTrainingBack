from pydantic import BaseModel

class AchievementBase(BaseModel):
    title: str
    body: str

class AchievementCreate(AchievementBase):
    pass

class Achievement(AchievementBase):
    id: int

    class Config:
        orm_mode = True
