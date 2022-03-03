from typing import List

from sqlalchemy.orm import Session

from ...repos.entities import Repo
from ...repos.repositories.crud_repo import CRUDRepo
from ..repositories import GitRepo


class RepoStore:
    @classmethod
    def all(cls, db: Session) -> List[GitRepo]:
        repos: List[Repo] = CRUDRepo.all(db=db)
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

    @classmethod
    def clone_all(cls, db: Session):
        repos: List[Repo] = CRUDRepo.all(db=db)
        for repo in repos:
            gitrepo = GitRepo(repo)
            if not gitrepo.exists_locally:
                gitrepo.clone()
