from sqlalchemy import Column, ForeignKey, Integer, Table

from config.environment import Base

repos_contributors = Table(
    "repos_contributors",
    Base.metadata,
    Column("repo_id", Integer, ForeignKey("repos.id"), primary_key=True),
    Column(
        "collaborator_id", Integer, ForeignKey("collaborators.id"), primary_key=True
    ),
)
