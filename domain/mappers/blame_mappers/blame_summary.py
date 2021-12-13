from typing import Dict, List

from .blame_report import Reporter
from ..git_mappers import GitRepo
from ...entities import FolderSummary
from typing_helpers import Filename, PorcelainLineReport


class Summary:
    def __init__(self, gitrepo: GitRepo):
        self._gitrepo = gitrepo

    async def for_folder(self, folder_name: str) -> FolderSummary:
        blame_reports: Dict[Filename, List[PorcelainLineReport]] = await Reporter(
            self._gitrepo
        ).folder_report(folder_name)

        return FolderSummary(folder_name, blame_reports)
