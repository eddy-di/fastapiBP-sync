from datetime import timedelta
from typing import Annotated, Any

from fastapi import Depends
from fastapi.routing import APIRouter
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.auth.schemas.token import Login, TokenPair
from app.auth.schemas.users import User, UserCreate
from app.auth.utils import authenticate_user, create_token
from app.config.database import get_db
from app.models.models import Users

auth = APIRouter(
    tags=['Auth'],
    prefix='/auth'
)


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@auth.post(
    '/register',
    status_code=201,
    response_model=User
)
def register(
    db: Annotated[Session, Depends(get_db)],
    schema: UserCreate
) -> dict[str, Any]:
    new_user = Users(
        username=schema.username,
        password=bcrypt_context.hash(schema.password),
        email=schema.email,
        first_name=schema.first_name,
        last_name=schema.last_name,
        is_active=schema.is_active,
        is_superuser=schema.is_superuser,
        role=schema.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'first_name': new_user.first_name,
        'last_name': new_user.last_name,
        'is_active': new_user.is_active,
        'is_superuser': new_user.is_superuser,
        'role': new_user.role,
    }


@auth.post(
    '/token',
    response_model=TokenPair
)
def obtain_token_pair(
    schema: Login,
    db: Annotated[Session, Depends(get_db)]
):
    user = authenticate_user(
        username=schema.username,
        password=schema.password,
        db=db
    )

    access_token = create_token(user.username, user.id, timedelta(hours=1))
    refresh_token = create_token(user.username, user.id, timedelta(days=1))

    return TokenPair(
        access=access_token,
        refresh=refresh_token
    )
