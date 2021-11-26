from pydantic import BaseModel
from typing import TypedDict, TypeVar, Dict


ContributorEmail = TypeVar("ContributorEmail", bound=str)
SubfolderName = TypeVar("SubfolderName", bound=str)
Filename = TypeVar("Filename", bound=str)


class Contribution(TypedDict):
    name: str
    count: int


# Represents folder summary about repo's folder
class FolderSummaryRepresenter(BaseModel):
    folder_name: str
    subfolders: Dict[SubfolderName, Dict[ContributorEmail, Contribution]]
    base_files: Dict[Filename, Dict[ContributorEmail, Contribution]]
