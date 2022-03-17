import os
import sys

WORKDIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(WORKDIR)

from app.application.services import LoadFromGithub
from app.domain.repos import entities as repo_entities
from app.domain.repos import mappers as repo_mappers
from app.domain.repos import repositories as repo_repositories
from app.domain.summary import entities as summary_entities
from app.domain.summary import mappers as summary_mappers
from app.domain.summary import repositories as summary_repositories
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

    db = SessionLocal()
