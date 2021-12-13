from typing import List
from sqlalchemy.orm import Session

from .crud_repo import CRUDRepo
from ..mappers.git_mappers import GitRepo
from .. import entities


class RepoStore:
    @classmethod
    def all(cls, db: Session) -> List[GitRepo]:
        repos: List[entities.Repo] = CRUDRepo.all(db=db)
        return list(
            filter(
                lambda gitrepo: gitrepo.exists_locally,
                map(lambda repo: GitRepo(repo), repos),
            )
        )

    @classmethod
    def delete_all(cls, db: Session) -> None:
        gitrepos: List[GitRepo] = cls.all(db=db)
        for gitrepo in gitrepos:
            gitrepo.delete()
