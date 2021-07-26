from typing import List

from ..api import API
from ...entities.contributor import Contributor


# Data Mapper for Github contributors
class ContributorMapper:
    def __init__(self, gateway: API):
        self._gateway = gateway

    def load_several(self, url: str) -> List[Contributor]:
        contribs_data = self._gateway.contributors_data(url)
        contribs_data = list(
            map(
                lambda contributor_data: self.build_entity(contributor_data),
                contribs_data,
            )
        )
        return contribs_data

    @classmethod
    def build_entity(cls, contributor_data: dict) -> Contributor:
        return _DataMapper(contributor_data).build_entity()


# Extracts entity specific elements from data structure
class _DataMapper:
    def __init__(self, contributor_data: dict):
        self._contributor = contributor_data

    def build_entity(self) -> Contributor:
        return Contributor(username=self.username, email=self.email)

    @property
    def username(self) -> str:
        return self._contributor["login"]

    @property
    def email(self) -> str:
        return self._contributor.get("email", None)
