import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_URL: str
    GH_TOKEN: str
    REPOSTORE_PATH: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    CLONE_QUEUE: str

    # The maximum repo size for cloning and analysis (unit: KB).
    # A value of zero means there's no such limit.
    MAX_CLONE_SIZE: int = 0


class Test(Settings):
    environment = "test"
    DB_FILENAME: str

    class Config:
        env_file = "config/env/test.env"
        env_file_encoding = "utf-8"
        secrets_dir = "config/secrets/test"


class Development(Settings):
    environment = "development"
    DB_FILENAME: str
    REPORT_QUEUE: str

    class Config:
        env_file = "config/env/dev.env"
        env_file_encoding = "utf-8"
        secrets_dir = "config/secrets/dev"


class Production(Settings):
    environment = "production"
    DATABASE_URL: str
    REDIS_URL: str
    REPORT_QUEUE: str

    class Config:
        env_file = "config/env/prod.env"
        env_file_encoding = "utf-8"
        secrets_dir = "config/secrets/prod"


@lru_cache()
def get_settings(mode: str = None, **kwargs) -> Settings:
    env = mode if mode else os.getenv("ENV", "development")
    return {"test": Test, "development": Development, "production": Production,}.get(
        env
    )(**kwargs)
