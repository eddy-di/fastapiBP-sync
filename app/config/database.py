from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.core import database_url

engine = create_engine(database_url)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)


def get_db() -> Generator[SessionLocal | Any | None]:  # type: ignore
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
