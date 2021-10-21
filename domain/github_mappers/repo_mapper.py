from typing import List, Type

from .collaborator_mapper import CollaboratorMapper
from .. import entities
from config import Settings
from infrastructure import github


# Data Mapper object for Github's git repos
class RepoMapper:
    def __init__(self, config: Settings, gateway_class: Type[github.API] = github.API):
        self._config = config
        self._gateway_class = gateway_class
        self._gateway = self._gateway_class(self._config.GH_TOKEN)

    def find(self, owner_name: str, repo_name: str) -> entities.Repo:
        data = self._gateway.repo_data(owner_name, repo_name)
        return self._build_entity(data)

    def _build_entity(self, data: dict) -> entities.Repo:
        return _DataMapper(data, self._config, self._gateway_class).build_entity()


# Extracts entity specific elements from data structure
class _DataMapper:
    def __init__(
        self,
        data: dict,
        config: Settings,
        gateway_class: Type[github.API] = github.API,
    ):
        self._data = data
        self._contributor_mapper = CollaboratorMapper(config, gateway_class)

    def build_entity(self) -> entities.Repo:
        return entities.Repo(
            id=None,
            origin_id=self.origin_id,
            name=self.name,
            size=self.size,
            owner=self.owner,
            git_url=self.git_url,
            contributors=self.contributors,
        )

    @property
    def origin_id(self) -> int:
        return self._data["id"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def size(self) -> int:
        return self._data["size"]

    @property
    def owner(self) -> entities.Collaborator:
        return CollaboratorMapper.build_entity(self._data["owner"])

    @property
    def git_url(self) -> str:
        return self._data["git_url"]

    @property
    def contributors(self) -> List[entities.Collaborator]:
        return self._contributor_mapper.load_several(self._data["contributors_url"])
