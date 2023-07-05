from datetime import datetime, timedelta
from jose import jwt, JWTError
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from models.user import User
from database import get_db

ALGORITHM = "HS256"  # Алгоритм шифрования JWT
SECRET_KEY = "your-secret-key"
JWT_EXPIRATION = timedelta(minutes=30)
REFRESH_TOKEN_EXPIRATION = timedelta(days=30)

def is_valid_google_token(token):
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request())
        return True
    except ValueError:
        return False


def create_jwt_token(user_id: int) -> str:
    now = datetime.utcnow()
    payload = {
        "user_id": user_id,
        "iat": now,
        "exp": now + JWT_EXPIRATION
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def create_refresh_token(user_id: int) -> str:
    now = datetime.utcnow()
    payload = {
        "user_id": user_id,
        "iat": now,
        "exp": now + REFRESH_TOKEN_EXPIRATION
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_user_by_google_token(token: str,db: Session = Depends(get_db)):
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request())
        email = id_info['email']
        user = db.query(User).filter(User.email == email).first()

        if user:
            return user

        new_user = User(email=email, username=id_info['name'])
        db.add(new_user)
        db.commit()
        return new_user

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_user_by_access_token(access_token: str, db: Session = Depends(get_db)):
    try:
        # Расшифровка access token и проверка его валидности
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

        # Получение пользователя из базы данных по user_id
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user

    except JWTError:
        # В случае невалидного access token, вызываем исключение HTTPException с кодом 401
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

def get_user_by_refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        # Расшифровка refresh token и проверка его валидности
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        # Получение пользователя из базы данных по user_id
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user

    except JWTError:
        # В случае невалидного refresh token, вызываем исключение HTTPException с кодом 401
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")