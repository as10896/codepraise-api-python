from typing import Any

from returns.result import Failure, Result, Success

from ...domain import entities, repositories
from ...presentation.responses import ApiResult


# Service to find a repo from our database
class FindDatabaseRepo:
    def __call__(self, **input: Any) -> Result[ApiResult, ApiResult]:
        repo = repositories.For[entities.Repo].find_full_name(
            input["db"], input["ownername"], input["reponame"]
        )
        if repo:
            return Success(ApiResult("ok", repo))
        else:
            return Failure(
                ApiResult("not_found", "Could not find stored git repository")
            )
