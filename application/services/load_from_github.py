from typing import Any, Dict
from returns.result import Result, Success, Failure
from returns.pipeline import flow
from returns.pointfree import bind

from domain import repositories
from domain.mappers import github_mappers
from domain.values import ServiceResult


# Transaction to load repo from Github and save to database
class LoadFromGithub:
    def __call__(self, **input: Any) -> Result[ServiceResult, ServiceResult]:
        return flow(
            input,
            self.get_repo_from_github,
            bind(self.check_if_repo_already_loaded),
            bind(self.store_repo_in_repository),
        )

    def get_repo_from_github(
        self, input: Dict[str, Any]
    ) -> Result[Dict[str, Any], ServiceResult]:
        try:
            repo = github_mappers.RepoMapper(input["config"]).find(
                input["ownername"], input["reponame"]
            )
            return Success({"db": input["db"], "repo": repo})
        except:
            return Failure(
                ServiceResult("bad_request", "Remote git repository not found")
            )

    def check_if_repo_already_loaded(
        self, input: Dict[str, Any]
    ) -> Result[Dict[str, Any], ServiceResult]:
        if repositories.For[type(input["repo"])].find(input["db"], input["repo"]):
            return Failure(ServiceResult("conflict", "Repo already loaded"))
        else:
            return Success(input)

    def store_repo_in_repository(
        self, input: Dict[str, Any]
    ) -> Result[ServiceResult, ServiceResult]:
        try:
            stored_repo = repositories.For[type(input["repo"])].create(
                input["db"], input["repo"]
            )
            return Success(ServiceResult("created", stored_repo))
        except Exception as e:
            print(e)
            return Failure(
                ServiceResult("internal_error", "Could not store remote repository")
            )
