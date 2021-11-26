from fastapi import APIRouter

from . import repo, summary


api_router = APIRouter()
api_router.include_router(repo.router, tags=["repo"])
api_router.include_router(summary.router, tags=["summary"])
