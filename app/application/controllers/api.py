from fastapi import APIRouter

from . import repo_controller, summary_controller

api_router = APIRouter()
api_router.include_router(repo_controller.router, tags=["repo"])
api_router.include_router(summary_controller.router, tags=["summary"])
