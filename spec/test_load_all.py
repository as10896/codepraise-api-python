import os
import sys

WORKDIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(WORKDIR)

from app.application.services import LoadFromGithub
from app.domain import entities, repositories
from app.domain.mappers import blame_mappers, git_mappers, github_mappers
from app.infrastructure import (
    database,  # necessary for SQLAlchemy to initialize relationships properly
)
from app.infrastructure import github, gitrepo
from config import get_settings
from config.environment import SessionLocal

if os.getenv("ENV") == "test":
    from config.environment import Base, engine

    Base.metadata.create_all(bind=engine)


# The following lines will be executed in console mode (`$ inv console`)
if __name__ == "__main__":

    from config.environment import SessionLocal

    db = SessionLocal()
