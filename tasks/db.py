from invoke import task
from config import get_settings


@task(help={"message": "Revision message of this migration."})
def revision(c, message):
    """
    Automatically generate migration script based on SQLAlchemy ORM models (manual review is necessary)
    """
    c.run(f"alembic revision --autogenerate -m {message}", pty=True)


@task(
    help={
        "env": "Environment of the database to migrate. ['test'|'development'|'production'] [default: 'development']"
    }
)
def migrate(c, env="development"):
    """
    Run migrations
    """
    import os

    os.environ["ENV"] = env

    print(f"Migrating {get_settings().environment} database to latest")

    if env == "test":
        from infrastructure.database import (
            orm,
        )  # necessary for SQLAlchemy to initialize relationships properly
        from config.environment import engine, Base

        Base.metadata.create_all(bind=engine)
    else:
        c.run(f"ENV={env} alembic upgrade head", pty=True)


@task(
    help={
        "env": "Environment of the database to drop all tables. ['test'|'development'|'production'] [default: 'development']"
    }
)
def drop(c, env="development"):
    """
    Drop all tables
    """
    import os

    os.environ["ENV"] = env

    print(f"Dropping all tables of {get_settings().environment} database")

    if env == "test":
        from infrastructure.database import (
            orm,
        )  # necessary for SQLAlchemy to initialize relationships properly
        from config.environment import engine, Base

        Base.metadata.drop_all(bind=engine)
    else:
        c.run(f"ENV={env} alembic downgrade base", pty=True)


@task(
    help={
        "env": "Environment of the database to reset. ['test'|'development'|'production'] [default: 'development']"
    }
)
def reset(c, env="development"):
    """
    Reset all database tables
    """
    drop(c, env)
    migrate(c, env)


@task(
    help={
        "env": "Environment of the database to delete. ['test'|'development'|'production'] [default: 'development']"
    }
)
def wipe(c, env="development"):
    """
    Delete dev or test database file
    """
    import os

    os.environ["ENV"] = env

    config = get_settings()

    if config.environment == "production":
        print("Cannot wipe production database!")
        return

    result = c.run(f"rm {config.DB_FILENAME}", hide=True, warn=True)
    if result.ok:
        print(f"Deleted #{config.DB_FILENAME}")
    else:
        print("No database file found")
