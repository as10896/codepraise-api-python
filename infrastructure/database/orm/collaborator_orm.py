from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from config.environment import Base
from .repos_collaborators_orm import repos_contributors
from .orm_repr_mixin import ORMReprMixin


class CollaboratorORM(Base, ORMReprMixin):
    __tablename__ = "collaborators"

    id = Column(Integer, primary_key=True, index=True)
    origin_id = Column(Integer, unique=True)

    username = Column(String, unique=True, nullable=False)
    email = Column(String)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    owned_repos = relationship("RepoORM", back_populates="owner")
    contributed_repos = relationship(
        "RepoORM", secondary=repos_contributors, back_populates="contributors"
    )

    def __repr__(self):
        return self._repr(
            id=self.id,
            origin_id=self.origin_id,
            username=self.username,
            email=self.email,
            created_at=self.created_at,
            updated_at=self.updated_at,
            owned_repos=list(map(lambda repo: repo.name, self.owned_repos)),
            contributed_repos=list(map(lambda repo: repo.name, self.contributed_repos)),
        )
