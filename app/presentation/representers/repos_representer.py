from typing import List

from pydantic import BaseModel

from .repo_representer import RepoRepresenter


# Represents essential Repo information for API output
class ReposRepresenter(BaseModel):
    repos: List[RepoRepresenter]
