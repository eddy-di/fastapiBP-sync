from typing import Annotated, Any

from fastapi import Depends
from fastapi.routing import APIRouter
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.auth.schemas import User, UserCreate
from app.config.database import get_db
from app.models.users import Users

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
        password=schema.password,
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
        'password': new_user.password,
        'email': new_user.email,
        'first_name': new_user.first_name,
        'last_name': new_user.last_name,
        'is_active': new_user.is_active,
        'is_superuser': new_user.is_superuser,
        'role': new_user.role,
    }
