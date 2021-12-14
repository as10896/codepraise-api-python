from typing import Any

from returns.result import Failure, Result, Success

from domain import entities, repositories
from domain.values import ServiceResult


# Service to find a repo from our database
class FindDatabaseRepo:
    def __call__(self, **input: Any) -> Result[ServiceResult, ServiceResult]:
        repo = repositories.For[entities.Repo].find_full_name(
            input["db"], input["ownername"], input["reponame"]
        )
        if repo:
            return Success(ServiceResult("ok", repo))
        else:
            return Failure(
                ServiceResult("not_found", "Could not find stored git repository")
            )
