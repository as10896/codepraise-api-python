from typing import Iterator

from .spec_helper import *


@pytest.fixture(scope="session")
def db() -> Iterator[SessionLocal]:
    _db = SessionLocal()
    try:
        yield _db
    finally:
        _db.close()
