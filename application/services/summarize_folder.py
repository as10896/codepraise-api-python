from typing import Any, Dict

from returns.future import FutureFailure, FutureResult, FutureSuccess
from returns.io import IOResult
from returns.pipeline import flow
from returns.pointfree import bind_async
from returns.result import Failure, Result, Success
from returns.unsafe import unsafe_perform_io

from domain.entities.folder_summary import FolderSummary
from domain.mappers.blame_mappers import Summary
from domain.mappers.git_mappers import GitRepo
from domain.values import ServiceResult
from workers import CloneRepoWorker

from ..representers import RepoRepresenter


class SummarizeFolder:
    async def __call__(self, **input: Any) -> Result[ServiceResult, ServiceResult]:
        future_result: FutureResult[ServiceResult, ServiceResult] = flow(
            input,
            self.clone_or_find_repo,
            FutureResult.from_result,
            bind_async(self.summarize_folder),
        )
        io_result: IOResult[
            ServiceResult, ServiceResult
        ] = await future_result.awaitable()

        return unsafe_perform_io(io_result)

    def clone_or_find_repo(
        self, input: Dict[str, Any]
    ) -> Result[Dict[str, Any], ServiceResult]:
        input["gitrepo"] = GitRepo(input["repo"])

        if input["gitrepo"].exists_locally:
            return Success(input)
        else:
            repo_json: str = RepoRepresenter.parse_obj(input["repo"]).json()
            try:
                CloneRepoWorker.clone_repo.delay(repo_json)
                return Failure(
                    ServiceResult("processing", "Processing the summary request")
                )
            except:
                return Failure(ServiceResult("internal_error", "Could not clone repo"))

    async def summarize_folder(
        self, input: Dict[str, Any]
    ) -> FutureResult[ServiceResult, ServiceResult]:
        try:
            folder_summary: FolderSummary = await Summary(input["gitrepo"]).for_folder(
                input["folder"]
            )
            return FutureSuccess(ServiceResult("ok", folder_summary))
        except:
            return FutureFailure(
                ServiceResult("internal_error", "Could not summarize folder")
            )
