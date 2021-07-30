import requests


# Library for Github Web API
class API:
    class Errors:
        # Not allowed to access resource
        class NotFound(Exception):
            pass

        # Requested resource not found
        class Unauthorized(Exception):
            pass

    def __init__(self, token: str):
        self.gh_token = token

    def repo_data(self, username: str, repo_name: str) -> dict:
        repo_req_url = self._gh_api_path(f"{username}/{repo_name}")
        return self._call_gh_url(repo_req_url).json()

    def contributors_data(self, contributors_url: str) -> dict:
        return self._call_gh_url(contributors_url).json()

    def _gh_api_path(self, path: str) -> str:
        return f"https://api.github.com/repos/{path}"

    def _call_gh_url(self, url: str) -> requests.models.Response:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.gh_token}",
        }

        response = requests.get(url, headers=headers)

        return _Response(response).response_or_error()


# Encapsulates API response success and errors
class _Response:
    HTTP_ERROR = {401: API.Errors.Unauthorized, 404: API.Errors.NotFound}

    def __init__(self, response):
        self.response = response

    def successful(self) -> bool:
        return self.response.status_code not in self.HTTP_ERROR

    def response_or_error(self) -> requests.models.Response:
        if self.successful():
            return self.response
        raise self.HTTP_ERROR[self.response.status_code]


if __name__ == "__main__":
    import os
    import yaml

    WORKDIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    with open(os.path.join(WORKDIR, "config/secrets.yml")) as f:
        CONFIG = yaml.safe_load(f)
    api = API(token=CONFIG["gh_token"])
    r = api.repo_data("as10896", "LessErrors")
    print(r["git_url"])
    try:
        r = api.repo_data("as10896", "foobar")
        print(r["git_url"])
    except API.Errors.NotFound:
        print("Repo Not Found")
