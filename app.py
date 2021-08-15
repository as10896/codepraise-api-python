from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from config import get_settings
from config.environment import get_db
from domain import github_mappers, entities
from domain import database_repositories as repository


config = get_settings()
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": f"CodePraise API v0.1 up in {config.environment} mode"}


@app.get("/api/v0.1/repo/{ownername}/{reponame}")
def repo_info(ownername: str, reponame: str, db: Session = Depends(get_db)):
    repo = repository.For[entities.Repo].find_full_name(db, ownername, reponame)
    if not repo:
        raise HTTPException(status_code=404, detail={"error": "Repository not found"})
    return repo


@app.post("/api/v0.1/repo/{ownername}/{reponame}")
def repo_info(
    ownername: str, reponame: str, response: Response, db: Session = Depends(get_db)
):
    try:
        repo = github_mappers.RepoMapper(config).load(ownername, reponame)
    except:
        raise HTTPException(status_code=404, detail={"error": "Repo not found"})

    stored_repo = repository.For[type(repo)].find_or_create(db, repo)
    response.status_code = 201
    response.headers["Location"] = f"/api/v0.1/repo/{ownername}/{reponame}"

    return stored_repo
