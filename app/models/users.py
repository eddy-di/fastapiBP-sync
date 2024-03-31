from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from app.models import Base


class RoleEnum(PyEnum):
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
