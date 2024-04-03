from pydantic import BaseModel, EmailStr

from app.models.models import RoleEnum


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    role: RoleEnum | None = RoleEnum.USER


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool | None = None
    role: RoleEnum | None = None
