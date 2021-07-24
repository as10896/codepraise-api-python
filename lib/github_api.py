import requests
from typing import List

from .repo import Repo
from .contributor import Contributor


class GithubAPI:

    class Errors:
        class NotFound(Exception): pass
        class Unauthorized(Exception): pass

    HTTP_ERROR = {
        401: Errors.Unauthorized,
        404: Errors.NotFound
    }

    def __init__(self, token: str, cache: dict = {}):
        self.gh_token = token
        self.cache = cache

    def repo(self, username: str, repo_name: str) -> Repo:
        repo_req_url = self._gh_api_path(f"{username}/{repo_name}")
        repo_data = self._call_gh_url(repo_req_url).json()
        return Repo(repo_data, self)

    def contributors(self, contributors_url: str) -> List[Contributor]:
        contributors_data = self._call_gh_url(contributors_url).json()
        contributors_data = list(map(lambda account_data: Contributor(account_data), contributors_data))
        return contributors_data

    def _gh_api_path(self, path: str) -> str:
        return f"https://api.github.com/repos/{path}"

    def _call_gh_url(self, url: str) -> requests.models.Response:
        if url in self.cache:
            return self.cache[url]

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.gh_token}"
        }

        result = requests.get(url, headers=headers)
        
        if self._successful(result):
            return result
        else:
            self._raise_error(result)

    @classmethod
    def _successful(cls, result) -> bool:
        return result.status_code not in cls.HTTP_ERROR

    @classmethod
    def _raise_error(cls, result):
        raise cls.HTTP_ERROR[result.status_code]
