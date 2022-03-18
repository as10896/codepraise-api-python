from typing import Iterator

from sqlalchemy.orm import Session

from .helper import *


@pytest.fixture(scope="session")
def db() -> Iterator[Session]:
    _db = SessionLocal()
    try:
        yield _db
    finally:
        _db.close()
