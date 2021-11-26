from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from returns.result import Result
from returns.pipeline import is_successful

from config.environment import get_db
from domain import entities
from domain.blame_reporter import Summary
from ..services import FindDatabaseRepo
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
    status_code=200,
)
def summary_for_entire_repo(repo: entities.Repo = Depends(find_repo)):
    folder_summary: entities.FolderSummary = Summary(repo).for_folder("")
    return {
        "folder_name": folder_summary.folder_name,
        "subfolders": folder_summary.subfolders,
        "base_files": folder_summary.base_files,
    }


@router.get(
    "/summary/{ownername}/{reponame}/{folder:path}",
    response_model=FolderSummaryRepresenter,
    status_code=200,
)
def summary_for_specific_folder(folder: str, repo: entities.Repo = Depends(find_repo)):
    folder_summary: entities.FolderSummary = Summary(repo).for_folder(folder)
    return {
        "folder_name": folder_summary.folder_name,
        "subfolders": folder_summary.subfolders,
        "base_files": folder_summary.base_files,
    }
