from fastapi import FastAPI

from config import get_settings

from .controllers import api_router, clone_progress_publisher

config = get_settings()
app = FastAPI()
app.include_router(api_router, prefix="/api/v0.1")
app.include_router(clone_progress_publisher.router)


@app.get("/")
async def read_root():
    return {"message": f"CodePraise API v0.1 up in {config.environment} mode"}
