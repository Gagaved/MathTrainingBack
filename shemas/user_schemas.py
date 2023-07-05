from pydantic import BaseModel
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass
class User(UserBase):
    id: int

    class Config:
        orm_mode = True
