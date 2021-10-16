from typing import List, Optional, ClassVar
from pydantic import BaseModel, StrictInt, StrictStr

from .collaborator import Collaborator
from .blame_summary import FolderSummary


# Domain entity object for any git repos
class Repo(BaseModel):
    id: Optional[int]
    origin_id: StrictInt
    name: StrictStr
    size: StrictInt
    git_url: StrictStr
    owner: Collaborator
    contributors: List[Collaborator]

    _MAX_SIZE: ClassVar[int] = 1000

    class Config:
        orm_mode = True

    @property
    def summarizable(self) -> bool:
        self.size < self._MAX_SIZE

    def folder_summary(self, folder_name: str) -> Optional[FolderSummary]:
        from ..blame_reporter import Summary

        if self.summarizable:
            return Summary(self).for_folder(folder_name)
