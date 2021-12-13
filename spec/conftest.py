from .spec_helper import *


@pytest.fixture(scope="session")
def db():
    _db = SessionLocal()
    try:
        yield _db
    finally:
        _db.close()
