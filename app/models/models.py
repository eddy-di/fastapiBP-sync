from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base(metadata=MetaData())


class RoleEnum(Enum):
    USER = 1
    STAFF = 2


class Users(Base):  # type: ignore
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    joined_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    role = Column(ENUM(RoleEnum, name='role_enum'), default=RoleEnum.USER)

    token = relationship('TokenBlacklist', back_populates='user')


class TokenBlacklist(Base):  # type: ignore
    __tablename__ = 'token_blacklist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(500), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    user = relationship('Users', back_populates='token')
