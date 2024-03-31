from datetime import datetime

from pydantic import BaseModel


class TokenBlacklistBase(BaseModel):  # type: ignore
    token: str
    expires_at: datetime
    user_id: int


class TokenBlacklistCreate(TokenBlacklistBase):
    pass


class TokenPair(BaseModel):
    access: str
    refresh: str
    token_type: str = 'Bearer'


class Login(BaseModel):
    username: str
    password: str
