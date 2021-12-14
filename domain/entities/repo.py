from typing import List, Optional

from pydantic import BaseModel, StrictInt, StrictStr

from .collaborator import Collaborator


# Domain entity object for any git repos
class Repo(BaseModel):
    id: Optional[int]
    origin_id: StrictInt
    name: StrictStr
    size: StrictInt
    git_url: StrictStr
    owner: Collaborator
    contributors: List[Collaborator]

    class Config:
        orm_mode = True
