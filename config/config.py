import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    gh_token: str


class Test(Settings):
    environment = "test"
    db_filename: str
    repostore_path: str

    class Config:
        env_file = "config/env/.env"
        env_file_encoding = "utf-8"
        secrets_dir = "config/secrets/test"


class Development(Settings):
    environment = "development"
    db_filename: str
    repostore_path: str

    class Config:
        env_file = "config/env/.env.dev"
        env_file_encoding = "utf-8"
        secrets_dir = "config/secrets/dev"


class Production(Settings):
    environment = "production"
    database_url: str

    class Config:
        env_file = "config/env/.env.prod"
        env_file_encoding = "utf-8"
        secrets_dir = "config/secrets/prod"


@lru_cache()
def get_settings(mode: str = None, **kwargs) -> Settings:
    env = mode if mode else os.getenv("ENV", "test")
    return {"test": Test, "development": Development, "production": Production,}.get(
        env
    )(**kwargs)
