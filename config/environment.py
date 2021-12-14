from typing import Generator

from sqlalchemy.ext.declarative import declarative_base

from .db_session import get_session_maker, get_sqlalchemy_engine

engine = get_sqlalchemy_engine()
SessionLocal = get_session_maker(engine)

Base = declarative_base()


# Dependency
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
