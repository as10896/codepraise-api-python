import requests
from typing import List

from .repo import Repo
from .contributor import Contributor


class Errors:
    # Not allowed to access resource
    class NotFound(Exception): pass
    # Requested resource not found
    class Unauthorized(Exception): pass


# Encapsulates API response success and errors
class _Response:
    HTTP_ERROR = {
        401: Errors.Unauthorized,
        404: Errors.NotFound
    }

    def __init__(self, response):
        self.response = response

    def successful(self) -> bool:
        return self.response.status_code not in self.HTTP_ERROR

    def response_or_error(self) -> requests.models.Response:
        if self.successful():
            return self.response
        raise self.HTTP_ERROR[self.response.status_code]


# Library for Github Web API
class GithubAPI:

    def __init__(self, token: str):
        self.gh_token = token

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
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.gh_token}"
        }

        response = requests.get(url, headers=headers)

        return _Response(response).response_or_error()
