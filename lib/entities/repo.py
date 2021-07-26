from typing import List
from pydantic import BaseModel, StrictInt, StrictStr

from .contributor import Contributor


class Repo(BaseModel):
    size: StrictInt
    owner: Contributor
    git_url: StrictStr
    contributors: List[Contributor]
