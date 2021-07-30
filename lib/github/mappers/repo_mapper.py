from typing import List

from .contributor_mapper import ContributorMapper
from ..api import API
from ...entities.repo import Repo
from ...entities.contributor import Contributor


# Data Mapper object for Github's git repos
class RepoMapper:
    def __init__(self, gateway: API):
        self._gateway = gateway

    def load(self, owner_name: str, repo_name: str) -> Repo:
        repo_data = self._gateway.repo_data(owner_name, repo_name)
        return self._build_entity(repo_data)

    def _build_entity(self, repo_data: dict) -> Repo:
        return _DataMapper(repo_data, self._gateway).build_entity()


# Extracts entity specific elements from data structure
class _DataMapper:
    def __init__(self, repo_data: dict, gateway: API):
        self._repo_data = repo_data
        self._contributor_mapper = ContributorMapper(gateway)

    def build_entity(self) -> Repo:
        return Repo(
            size=self.size,
            owner=self.owner,
            git_url=self.git_url,
            contributors=self.contributors,
        )

    @property
    def size(self) -> int:
        return self._repo_data["size"]

    @property
    def owner(self) -> Contributor:
        return ContributorMapper.build_entity(self._repo_data["owner"])

    @property
    def git_url(self) -> str:
        return self._repo_data["git_url"]

    @property
    def contributors(self) -> List[Contributor]:
        return self._contributor_mapper.load_several(
            self._repo_data["contributors_url"]
        )
