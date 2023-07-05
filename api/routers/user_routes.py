from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from main import get_db
from models.user import User
from shemas.user_schemas import UserCreate

router = APIRouter()


@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        # Пользователь уже существует, возвращаем ошибку
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"username": new_user.username, "email": new_user.email}


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        # Пользователь не найден, возвращаем ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}

@router.get("/users/{user_id}")
def get_user(user_id: int,db: Session = Depends(get_db)):
    # Получение пользователя из базы данных по ID
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        # Возврат ответа с информацией о пользователе
        return {"username": user.username, "email": user.email}
    else:
        # Возврат ответа с сообщением об отсутствии пользователя
        return {"message": "User not found"}

