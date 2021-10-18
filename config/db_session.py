import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import Settings, get_settings


def get_db_url(config: Settings = get_settings()) -> str:

    if config.environment in ["test", "development"]:
        DATABASE_URL = f"sqlite:///{config.db_filename}"

    elif config.environment == "production":
        # Will first look for the DATABASE_URL environment variable
        # If not found, then look for the `config/secrets/prod/database_url`

        # Note: don't specify if you're using Heroku Postgres
        # cause Heroku has its own DATABASE_URL environment variable
        DATABASE_URL = config.database_url

        # SQLAlchemy 1.4.x has removed support for the "postgres://" URI scheme, which is used by Heroku Postgres
        # replace it with "postgresql://" to maintain compatibility
        # Ref: https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace(
                "postgres://", "postgresql+psycopg2://", 1
            )

    return DATABASE_URL


def get_sqlalchemy_engine(
    config: Settings = get_settings(),
) -> sqlalchemy.engine.base.Engine:

    DATABASE_URL = get_db_url(config)

    if config.environment == "production":
        engine = create_engine(DATABASE_URL)
    else:
        # {"check_same_thread": False} is needed only for SQLite
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    return engine


def get_session_maker(engine: sqlalchemy.engine.base.Engine) -> sessionmaker:
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
