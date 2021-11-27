from pydantic import BaseModel
from typing import Dict

from typing_helpers import Filename, SubfolderName, ContributorEmail, Contribution


# Represents folder summary about repo's folder
class FolderSummaryRepresenter(BaseModel):
    folder_name: str
    subfolders: Dict[SubfolderName, Dict[ContributorEmail, Contribution]]
    base_files: Dict[Filename, Dict[ContributorEmail, Contribution]]
