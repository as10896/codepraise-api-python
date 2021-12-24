from pydantic import BaseModel

from .repo_representer import RepoRepresenter


class CloneRequestRepresenter(BaseModel):
    repo: RepoRepresenter
    id: int
