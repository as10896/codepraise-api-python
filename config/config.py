import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    gh_token: str


class Test(Settings):
    environment = "test"

    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"


class Development(Settings):
    environment = "development"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class Production(Settings):
    environment = "production"

    class Config:
        env_file = "config/prod.env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings(mode="test"):
    env = mode if mode else os.getenv("ENV", "test")
    return {
        "test": Test,
        "development": Development,
        "production": Production,
    }.get(env)()
