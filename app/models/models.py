from datetime import UTC, datetime

from sqlalchemy import (
    BOOLEAN,
    JSON,
    TIMESTAMP,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)

metadata = MetaData()


roles = Table(
    'roles',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(32), nullable=False),
    Column('permission', JSON)
)

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(32), nullable=False, unique=True),
    Column('password', String(200), nullable=False),
    Column('email', String(255), nullable=False, unique=True),
    Column('first_name', String(50), nullable=True),
    Column('last_name', String(50), nullable=True),
    Column('last_login', TIMESTAMP, default=datetime.now(UTC)),
    Column('is_active', BOOLEAN, nullable=False, default=True),
    Column('is_superuser', BOOLEAN, nullable=False, default=False),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'))
)

token_blacklist = Table(
    'token_blacklist',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('token', String(500), nullable=False),
    Column('expires_at', DateTime, nullable=False),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'))
)
