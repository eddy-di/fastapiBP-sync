from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.auth.configs import ALGORITHM, SECRET_KEY
from app.config.database import get_db
from app.models.models import RoleEnum, Users

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


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
    role: RoleEnum,
    expires_delta: timedelta
) -> str:
    encode = {'sub': username, 'id': user_id, 'role': role, }
    issued_at = datetime.now(timezone.utc)
    expires = issued_at + expires_delta
    encode.update({
        'iat': issued_at,
        'exp': expires
    })
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_db(username: str, db: Annotated[Session, Depends(get_db)]):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail='Could not validate user.')
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
    db: Annotated[Session, Depends(get_db)]
) -> Users | HTTPException:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')

        if username is None:
            raise HTTPException(status_code=401, detail='Could not validate users from token.')

    except JWTError:
        raise HTTPException(status_code=401, detail='Could not validate user token error.')

    user = get_user_from_db(username=username, db=db)

    return user


def get_current_token(
    token: Annotated[str, Depends(oauth2_bearer)]
) -> str:
    return token


def decode_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
