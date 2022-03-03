from pydantic import BaseModel

from .repo_representer import RepoRepresenter


# Representer object for repo clone requests
class CloneRequestRepresenter(BaseModel):
    repo: RepoRepresenter
    id: int
