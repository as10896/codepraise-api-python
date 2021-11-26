from typing import List, Optional, ClassVar
from pydantic import BaseModel, StrictInt, StrictStr

from .collaborator import Collaborator
from .folder_summary import FolderSummary


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

    class Errors:
        class TooLargeToSummarize(Exception):
            pass

    @property
    def too_large(self) -> bool:
        self.size > self._MAX_SIZE

    def folder_summary(self, folder_name: str) -> FolderSummary:
        if self.too_large:
            raise self.Errors.TooLargeToSummarize
        return FolderSummary(self.git_url, folder_name)
