from typing import Dict, List

from typing_helpers import Filename, PorcelainLineReport

from ...entities import FolderSummary
from ..git_mappers import GitRepo
from .blame_report import Reporter


class Summary:
    def __init__(self, gitrepo: GitRepo):
        self._gitrepo = gitrepo

    async def for_folder(self, folder_name: str) -> FolderSummary:
        blame_reports: Dict[Filename, List[PorcelainLineReport]] = await Reporter(
            self._gitrepo
        ).folder_report(folder_name)

        return FolderSummary(folder_name, blame_reports)
