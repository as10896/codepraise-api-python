import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import Settings, get_settings


def get_db_url(config: Settings = get_settings()) -> str:

    if config.environment in ["test", "development"]:
        DATABASE_URL = f"sqlite:///{config.db_filename}"

    elif config.environment == "production":
        # TODO: Use Heroku's DATABASE_URL environment variable
        DATABASE_URL = config.database_url

    return DATABASE_URL


def get_sqlalchemy_engine(
    config: Settings = get_settings(),
) -> sqlalchemy.engine.base.Engine:

    DATABASE_URL = get_db_url(config)

    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    return engine


def get_session_maker(engine: sqlalchemy.engine.base.Engine) -> sessionmaker:
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
