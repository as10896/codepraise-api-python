from typing import List, Optional, Type

from config import Settings

from ....infrastructure import github
from ... import entities


# Data Mapper for Github contributors
class CollaboratorMapper:
    def __init__(self, config: Settings, gateway_class: Type[github.API] = github.API):
        self._config = config
        self._gateway = gateway_class(self._config.GH_TOKEN)

    def load_several(self, url: str) -> List[entities.Collaborator]:
        contribs_data = self._gateway.collaborators_data(url)
        contribs_data = list(
            map(
                lambda data: self.build_entity(data),
                contribs_data,
            )
        )
        return contribs_data

    @classmethod
    def build_entity(cls, data: dict) -> entities.Collaborator:
        return _DataMapper(data).build_entity()


# Extracts entity specific elements from data structure
class _DataMapper:
    def __init__(self, data: dict):
        self._data = data

    def build_entity(self) -> entities.Collaborator:
        return entities.Collaborator(
            id=None, origin_id=self.origin_id, username=self.username, email=self.email
        )

    @property
    def origin_id(self) -> int:
        return self._data["id"]

    @property
    def username(self) -> str:
        return self._data["login"]

    @property
    def email(self) -> Optional[str]:
        return self._data.get("email", None)
