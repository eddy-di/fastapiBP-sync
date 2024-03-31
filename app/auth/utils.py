from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.auth.configs import ALGORITHM, SECRET_KEY
from app.config.database import get_db
from app.models.models import Users

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def authenticate_user(
    username: str,
    password: str,
    db: Annotated[Session, Depends(get_db)]
) -> HTTPException | Users:
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return HTTPException(status_code=401, detail='Could not validate user.')
    if not bcrypt_context.verify(password, user.password):
        return HTTPException(status_code=401, detail='Could not validate user.')
    return user


def create_token(
    username: str,
    user_id: int,
    expires_delta: timedelta
) -> str:
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
