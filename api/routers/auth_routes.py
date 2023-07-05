from fastapi import APIRouter
from fastapi import status

from api.utils.auth_utils import is_valid_google_token, create_jwt_token, get_user_by_google_token, \
    create_refresh_token, get_user_by_refresh_token
from database import get_db
from shemas.token_schemas import Token
from fastapi import HTTPException

router = APIRouter()


@router.post("/refresh_token", response_model=Token)
def refresh_token(refresh_token: str):
    # Проверка валидности refresh token и получение пользователя
    user = get_user_by_refresh_token(refresh_token)

    # Создание нового access token
    access_token = create_jwt_token(user.id)

    # Создание нового refresh token
    refresh_token = create_refresh_token(user.id)

    # Возвращение новых access token и refresh token
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


# Функция для получения пользователя по токену Google
@router.post("/token")
def login(token: str):
    if not is_valid_google_token(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google token")
    user = get_user_by_google_token(token)
    access_token = create_jwt_token(user.id)
    refresh_token = create_refresh_token(user.id)
    # Возвращаем токен пользователю
    return {"access_token": access_token, "refresh_token": refresh_token}
