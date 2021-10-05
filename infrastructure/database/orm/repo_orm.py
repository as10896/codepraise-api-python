from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from config.environment import Base
from .repos_collaborators_orm import repos_contributors
from .orm_repr_mixin import ORMReprMixin


class RepoORM(Base, ORMReprMixin):
    __tablename__ = "repos"

    id = Column(Integer, primary_key=True, index=True)
    origin_id = Column(Integer, unique=True)
    owner_id = Column(Integer, ForeignKey("collaborators.id"))

    name = Column(String)
    size = Column(Integer)
    git_url = Column(String)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    owner = relationship("CollaboratorORM", back_populates="owned_repos")
    contributors = relationship(
        "CollaboratorORM",
        secondary=repos_contributors,
        back_populates="contributed_repos",
    )

    def __repr__(self):
        return self._repr(
            id=self.id,
            origin_id=self.origin_id,
            owner_id=self.owner_id,
            name=self.name,
            size=self.size,
            git_url=self.git_url,
            created_at=self.created_at,
            updated_at=self.updated_at,
            owner=self.owner.username,
            contributors=list(map(lambda contrib: contrib.username, self.contributors)),
        )
