from fastapi import FastAPI, Depends, HTTPException

from config import config
from lib.github.api import API
from lib.github.mappers.repo_mapper import RepoMapper
from lib.entities.repo import Repo

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": f"CodePraise API v0.1 up in {config.get_settings().environment}"}


def get_repo(
    ownername: str,
    repo_name: str,
    config: config.Settings = Depends(config.get_settings),
) -> Repo:
    github_api = API(config.gh_token)
    repo_mapper = RepoMapper(github_api)
    try:
        repo = repo_mapper.load(ownername, repo_name)
    except:
        raise HTTPException(status_code=404, detail={"error": "Repo not found"})
    return repo


@app.get("/api/v0.1/repo/{ownername}/{repo_name}")
def repo_info(repo: Repo = Depends(get_repo)):
    return {"repo": {"owner": repo.owner.dict(), "size": repo.size}}


@app.get("/api/v0.1/repo/{ownername}/{repo_name}/{contributors}")
def contributors_info(repo: Repo = Depends(get_repo)):
    return {"contributors": list(map(lambda c: c.dict(), repo.contributors))}
