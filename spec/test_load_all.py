import os
import sys

WORKDIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(WORKDIR)

from config import get_settings

from domain import entities
from domain import github_mappers
from domain import database_repositories as repository

from infrastructure import github
from infrastructure import gitrepo
from infrastructure import (
    database,
)  # necessary for SQLAlchemy to initialize relationships properly


if os.getenv("ENV") == "test":
    from config.environment import engine, Base

    Base.metadata.create_all(bind=engine)


# The following lines will be executed in console mode (`$ inv console`)
if __name__ == "__main__":

    from config.environment import SessionLocal

    db = SessionLocal()
