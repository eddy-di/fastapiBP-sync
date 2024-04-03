from datetime import timedelta
from typing import Annotated, Any

from fastapi import Depends
from fastapi.routing import APIRouter
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.auth.schemas.token import Login, TokenPair
from app.auth.schemas.users import User, UserCreate, UserUpdate
from app.auth.utils import (
    authenticate_user,
    create_token,
    decode_token,
    get_current_token,
    get_current_user,
)
from app.config.database import get_db
from app.models.models import TokenBlacklist, Users

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

    access_token = create_token(user.username, user.id, user.role.value, timedelta(minutes=5))
    refresh_token = create_token(user.username, user.id, user.role.value, timedelta(days=1))

    return TokenPair(
        access=access_token,
        refresh=refresh_token
    )


@auth.get(
    '/profile',
    response_model=User,
    summary='Authenticated users profile'
)
def get_auth_current_user(
    user: Annotated[Users, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter(Users.id == user.id).first()
    return user


@auth.patch(
    '/profile',
    response_model=User,
    summary='Patch authenticated current user'
)
def pathc_auth_current_user(
    schema: UserUpdate,
    user: Annotated[Users, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    user = db.query(Users).filter(Users.id == user.id).first()

    patch_data = schema.model_dump(exclude_unset=True)

    for key, value in patch_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


@auth.delete(
    '/profile',
    summary='Delete authenticated current user',
    status_code=204
)
def delete_auth_current_user(
    user: Annotated[Users, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> None:
    user = db.query(Users).filter(Users.id == user.id).first()

    db.delete(user)
    db.commit()

    return None


@auth.post(
    '/logout',
    summary='Logs out user, token blacklisted',
    status_code=200
)
def logout_auth_current_user(
    token: str = Depends(get_current_token),
    db: Session = Depends(get_db),
):
    decoded_dict = decode_token(token)
    expires_at = decoded_dict['exp']
    token_to_be_blacklisted = TokenBlacklist(
        token=token,
        expires_at=expires_at
    )
    db.add(token_to_be_blacklisted)
    db.commit()
    db.refresh(token_to_be_blacklisted)
    return {
        'message': 'Logged out successfully.'
    }
