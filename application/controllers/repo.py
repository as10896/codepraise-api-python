from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from returns.result import Result
from returns.pipeline import is_successful

from config import get_settings
from config.environment import get_db

from infrastructure import database

from domain import entities
from domain import database_repositories as repository
from domain.values import ServiceResult

from ..services import LoadFromGithub, FindDatabaseRepo
from ..representers import RepoRepresenter, ReposRepresenter, HttpResponseRepresenter


config = get_settings()
router = APIRouter()


@router.get("/repo/", response_model=ReposRepresenter)
def find_all_database_repos(db: Session = Depends(get_db)):
    repos: List[entities.Repo] = repository.For[entities.Repo].all(db)
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


@router.get("/repo/{ownername}/{reponame}")
def find_database_repo(ownername: str, reponame: str, db: Session = Depends(get_db)):
    find_result: Result = FindDatabaseRepo()(
        db=db, ownername=ownername, reponame=reponame
    )
    if is_successful(find_result):
        find_result: ServiceResult = find_result.unwrap()

        http_response: HttpResponseRepresenter = HttpResponseRepresenter.parse_obj(
            find_result.dict()
        )

        # BaseModel.parse_obj() can just recieve another BaseModel, instead of a dict.
        # We could also do field filtering in this way, without using FastAPI's response_model parameter
        found_repo: entities.Repo = find_result.message
        response_content: RepoRepresenter = RepoRepresenter.parse_obj(found_repo)
        response_content: Dict[str, Any] = jsonable_encoder(response_content)

        return JSONResponse(
            status_code=http_response.http_code, content=response_content
        )
    else:
        find_result: ServiceResult = find_result.failure()
        http_response: HttpResponseRepresenter = HttpResponseRepresenter.parse_obj(
            find_result.dict()
        )
        return JSONResponse(
            status_code=http_response.http_code, content=http_response.http_message
        )


@router.post("/repo/{ownername}/{reponame}")
def load_from_github(ownername: str, reponame: str, db: Session = Depends(get_db)):
    service_result: Result = LoadFromGithub()(
        db=db, config=config, ownername=ownername, reponame=reponame
    )
    if is_successful(service_result):
        service_result: ServiceResult = service_result.unwrap()

        http_response: HttpResponseRepresenter = HttpResponseRepresenter.parse_obj(
            service_result.dict()
        )

        headers = {"Location": f"/api/v0.1/repo/{ownername}/{reponame}"}

        stored_repo: entities.Repo = service_result.message
        response_content: RepoRepresenter = RepoRepresenter.parse_obj(stored_repo)
        response_content: Dict[str, Any] = jsonable_encoder(response_content)

        return JSONResponse(
            status_code=http_response.http_code,
            content=response_content,
            headers=headers,
        )
    else:
        service_result: ServiceResult = service_result.failure()
        http_response: HttpResponseRepresenter = HttpResponseRepresenter.parse_obj(
            service_result.dict()
        )
        return JSONResponse(
            status_code=http_response.http_code, content=http_response.http_message
        )