from typing import Any, Dict

from returns.pipeline import flow
from returns.pointfree import bind
from returns.result import Failure, Result, Success

from ...domain.repos import repositories
from ...domain.repos.mappers import RepoMapper
from ...presentation.responses import ApiResult


# Transaction to load repo from Github and save to database
class LoadFromGithub:
    def __call__(self, **input: Any) -> Result[ApiResult, ApiResult]:
        return flow(
            input,
            self.get_repo_from_github,
            bind(self.check_if_repo_already_loaded),
            bind(self.store_repo_in_repository),
        )

    def get_repo_from_github(
        self, input: Dict[str, Any]
    ) -> Result[Dict[str, Any], ApiResult]:
        try:
            repo = RepoMapper(input["config"]).find(
                input["ownername"], input["reponame"]
            )
            return Success({"db": input["db"], "repo": repo})
        except:
            return Failure(ApiResult("bad_request", "Remote git repository not found"))

    def check_if_repo_already_loaded(
        self, input: Dict[str, Any]
    ) -> Result[Dict[str, Any], ApiResult]:
        if repositories.For[type(input["repo"])].find(input["db"], input["repo"]):
            return Failure(ApiResult("conflict", "Repo already loaded"))
        else:
            return Success(input)

    def store_repo_in_repository(
        self, input: Dict[str, Any]
    ) -> Result[ApiResult, ApiResult]:
        try:
            stored_repo = repositories.For[type(input["repo"])].create(
                input["db"], input["repo"]
            )
            return Success(ApiResult("created", stored_repo))
        except Exception as e:
            print(e)
            return Failure(
                ApiResult("internal_error", "Could not store remote repository")
            )
