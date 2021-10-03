from typing import List
from pydantic import BaseModel, StrictInt, StrictStr

from .collaborator_representer import CollaboratorRepresenter


# Represents essential Repo information for API output
class RepoRepresenter(BaseModel):
    origin_id: StrictInt
    owner: CollaboratorRepresenter
    name: StrictStr
    size: StrictInt
    git_url: StrictStr
    contributors: List[CollaboratorRepresenter]
