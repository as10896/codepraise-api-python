from typing import List

from . import github_api
from .contributor import Contributor


class Repo:
    def __init__(self, repo_data: dict, data_source: github_api.GithubAPI):
        self._repo = repo_data
        self._data_source = data_source

    @property
    def size(self) -> int:
        return self._repo["size"]

    @property
    def owner(self) -> Contributor:
        if not hasattr(self, "_owner"):
            self._owner = Contributor(self._repo["owner"])
        return self._owner

    @property
    def git_url(self) -> str:
        return self._repo["git_url"]

    @property
    def contributors(self) -> List[Contributor]:
        if not hasattr(self, "_contributors"):
            self._contributors = self._data_source.contributors(
                self._repo["contributors_url"]
            )
        return self._contributors
