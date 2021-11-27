from typing import Dict, List

from .blame_report import Reporter
from ..entities import Repo, FolderSummary
from typing_helpers import Filename, PorcelainLineReport


class Summary:

    _MAX_SIZE = 1000

    class Errors:
        class TooLargeToSummarize(Exception):
            pass

    def __init__(self, repo: Repo):
        self._repo = repo

    @property
    def too_large(self) -> bool:
        self._repo.size > self._MAX_SIZE

    def for_folder(self, folder_name: str) -> FolderSummary:
        if self.too_large:
            raise self.Errors.TooLargeToSummarize

        blame_reports: Dict[Filename, List[PorcelainLineReport]] = Reporter(
            self._repo
        ).folder_report(folder_name)

        return FolderSummary(folder_name, blame_reports)
