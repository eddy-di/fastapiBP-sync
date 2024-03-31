from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.users import RoleEnum


class RegisterUser(BaseModel):  # type: ignore
    username: str = Field(pattern=r'^[\w.-]+$')
    password: str
    email: EmailStr
    role: int | None = 1


class RegisterSuccess(BaseModel):  # type: ignore
    id: int
    username: str
    email: str
    role: int


class UserBase(BaseModel):  # type: ignore
    # username: str
    # password: str
    # email: EmailStr
    # first_name: str
    # last_name: str
    # is_active: bool
    # is_superuser: bool
    # role: RoleEnum
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    role: RoleEnum | None = RoleEnum.USER


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class TokenBlacklistBase(BaseModel):  # type: ignore
    token: str
    expires_at: datetime
    user_id: int


class TokenBlacklistCreate(TokenBlacklistBase):
    pass
