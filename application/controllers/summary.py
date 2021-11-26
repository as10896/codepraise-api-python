from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from returns.result import Result
from returns.pipeline import is_successful

from config.environment import get_db
from domain import entities
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
    summary: entities.FolderSummary = repo.folder_summary("")
    return {
        "folder_name": summary.folder_name,
        "subfolders": summary.subfolders,
        "base_files": summary.base_files,
    }


@router.get(
    "/summary/{ownername}/{reponame}/{folder:path}",
    response_model=FolderSummaryRepresenter,
    status_code=200,
)
def summary_for_specific_folder(folder: str, repo: entities.Repo = Depends(find_repo)):
    summary: entities.FolderSummary = repo.folder_summary(folder)
    return {
        "folder_name": summary.folder_name,
        "subfolders": summary.subfolders,
        "base_files": summary.base_files,
    }
