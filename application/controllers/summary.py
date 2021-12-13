from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from returns.result import Result
from returns.pipeline import is_successful
from datetime import datetime

from config.environment import get_db
from domain import entities
from .route_helpers import represent_response
from ..services import FindDatabaseRepo, SummarizeFolder
from ..representers import FolderSummaryRepresenter


router = APIRouter()


def find_repo(
    ownername: str, reponame: str, db: Session = Depends(get_db)
) -> entities.Repo:
    find_result: Result = FindDatabaseRepo()(
        db=db, ownername=ownername, reponame=reponame
    )
    if not is_successful(find_result):
        raise HTTPException(status_code=404, detail={"error": "Repo not found"})

    return find_result.unwrap().dict()["message"]


@router.get(
    "/summary/{ownername}/{reponame}",
    response_model=FolderSummaryRepresenter,
)
async def summary_for_entire_repo(
    request: Request, repo: entities.Repo = Depends(find_repo)
):
    request_unique = [dict(request), request.url.path, datetime.now()]
    request_id: int = hash("".join(map(str, request_unique)))

    summarize_result: Result = await SummarizeFolder()(
        repo=repo, folder="", unique_id=request_id
    )

    return represent_response(summarize_result, FolderSummaryRepresenter)


@router.get(
    "/summary/{ownername}/{reponame}/{folder:path}",
    response_model=FolderSummaryRepresenter,
)
async def summary_for_specific_folder(
    folder: str, request: Request, repo: entities.Repo = Depends(find_repo)
):
    request_unique = [dict(request), request.url.path, datetime.now()]
    request_id: int = hash("".join(map(str, request_unique)))

    summarize_result: Result = await SummarizeFolder()(
        repo=repo, folder=folder, unique_id=request_id
    )

    return represent_response(summarize_result, FolderSummaryRepresenter)
