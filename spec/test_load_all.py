import os
import sys

WORKDIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(WORKDIR)

from application.services import LoadFromGithub
from config import get_settings
from config.environment import SessionLocal
from domain import entities, repositories
from domain.mappers import blame_mappers, git_mappers, github_mappers
from infrastructure import (
    database,  # necessary for SQLAlchemy to initialize relationships properly
)
from infrastructure import github, gitrepo

if os.getenv("ENV") == "test":
    from config.environment import Base, engine

    Base.metadata.create_all(bind=engine)


# The following lines will be executed in console mode (`$ inv console`)
if __name__ == "__main__":

    from config.environment import SessionLocal

    db = SessionLocal()
