from typing import Any, Dict

from returns.future import FutureFailure, FutureResult, FutureSuccess
from returns.io import IOResult
from returns.pipeline import flow
from returns.pointfree import bind, bind_async
from returns.result import Failure, Result, Success
from returns.unsafe import unsafe_perform_io

from domain.entities.folder_summary import FolderSummary
from domain.mappers.blame_mappers import Summary
from domain.mappers.git_mappers import GitRepo
from domain.values import CloneRequest, ServiceResult
from workers import CloneRepoWorker

from ..representers import CloneRequestRepresenter


class SummarizeFolder:
    async def __call__(self, **input: Any) -> Result[ServiceResult, ServiceResult]:
        future_result: FutureResult[ServiceResult, ServiceResult] = flow(
            input,
            self.find_repo,
            bind(self.clone_repo),
            FutureResult.from_result,
            bind_async(self.summarize_folder),
        )
        io_result: IOResult[
            ServiceResult, ServiceResult
        ] = await future_result.awaitable()

        return unsafe_perform_io(io_result)

    def find_repo(self, input: Dict[str, Any]) -> Result[Dict[str, Any], None]:
        input["gitrepo"] = GitRepo(input["repo"])
        return Success(input)

    def clone_repo(
        self, input: Dict[str, Any]
    ) -> Result[Dict[str, Any], ServiceResult]:
        if input["gitrepo"].exists_locally:
            return Success(input)
        else:
            clone_request_json: str = self._clone_request_json(input).json()
            try:
                CloneRepoWorker.clone_repo.delay(clone_request_json)
                return Failure(ServiceResult("processing", {"id": input["id"]}))
            except Exception as error:
                print(f"ERROR: SummarizeFolder#clone_repo - {error}")
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

    def _clone_request_json(self, input: Dict[str, Any]) -> CloneRequestRepresenter:
        clone_request = CloneRequest(input["repo"], input["id"])
        return CloneRequestRepresenter.parse_obj(clone_request)
