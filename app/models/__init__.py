from app.models.token import TokenBlacklist
from app.models.users import Users
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

Base = declarative_base(metadata=MetaData())
