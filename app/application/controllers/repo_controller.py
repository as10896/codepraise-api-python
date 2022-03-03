from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from returns.result import Result
from sqlalchemy.orm import Session

from config import get_settings
from config.environment import get_db

from ...domain import entities, repositories
from ...domain.values import ServiceResult
from ...infrastructure import database
from ..representers import HttpResponseRepresenter, RepoRepresenter, ReposRepresenter
from ..services import FindDatabaseRepo, LoadFromGithub
from .route_helpers import represent_response

config = get_settings()
router = APIRouter()


@router.get("/repo/", response_model=ReposRepresenter)
def find_all_database_repos(db: Session = Depends(get_db)):
    repos: List[entities.Repo] = repositories.For[entities.Repo].all(db)
    return {"repos": repos}


if config.environment in ["test", "development"]:

    @router.delete("/repo/")
    def delete_all_database_repos(db: Session = Depends(get_db)):
        db.query(database.orm.CollaboratorORM).delete()
        db.query(database.orm.RepoORM).delete()
        db.query(database.orm.repos_contributors).delete()
        db.commit()

        result = ServiceResult("ok", "deleted tables")

        http_response: HttpResponseRepresenter = HttpResponseRepresenter.parse_obj(
            result.dict()
        )
        return JSONResponse(
            status_code=http_response.http_code, content=http_response.http_message
        )


@router.get("/repo/{ownername}/{reponame}", response_model=RepoRepresenter)
def find_database_repo(ownername: str, reponame: str, db: Session = Depends(get_db)):
    find_result: Result = FindDatabaseRepo()(
        db=db, ownername=ownername, reponame=reponame
    )
    return represent_response(find_result, RepoRepresenter)


@router.post("/repo/{ownername}/{reponame}", response_model=RepoRepresenter)
def load_from_github(ownername: str, reponame: str, db: Session = Depends(get_db)):
    load_result: Result = LoadFromGithub()(
        db=db, config=config, ownername=ownername, reponame=reponame
    )
    headers = {"Location": f"/api/v0.1/repo/{ownername}/{reponame}"}
    return represent_response(load_result, RepoRepresenter, headers=headers)
