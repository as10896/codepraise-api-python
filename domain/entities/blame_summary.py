from typing import Dict, List, Union
from itertools import starmap


# Summarizes a single file's blame report
class FileSummary:
    def __init__(
        self, filename: str, line_reports: List[Dict[str, Union[str, Dict[str, str]]]]
    ):
        self._filename = filename
        self._contributions = self._summarize_line_reports(line_reports)

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def contributions(self) -> Dict[str, Dict[str, Union[int, str]]]:
        return self._contributions

    def _summarize_line_reports(
        self, line_reports: List[Dict[str, Union[str, Dict[str, str]]]]
    ) -> Dict[str, Dict[str, Union[int, str]]]:
        contributions = {}
        for report in line_reports:
            if report["author-mail"] not in contributions:
                contributions[report["author-mail"]] = {
                    "name": report["author"],
                    "count": 0,
                }
            contributions[report["author-mail"]]["count"] += 1
        return contributions


# Summarizes blame reports for an entire folder
# TODO: exclude folders feature, refactor, file counts
class FolderSummary:
    def __init__(
        self,
        folder_name: str,
        blame_reports: Dict[str, List[Dict[str, Union[str, Dict[str, str]]]]],
    ):
        self._folder_name = folder_name
        self._blame_reports = blame_reports

    @property
    def folder_name(self) -> str:
        return self._folder_name

    @property
    def contributions(self) -> Dict[str, Dict[str, Union[int, str]]]:
        _contributions = {}
        for summary in self.file_summaries:
            for email, contribution in summary.contributions.items():
                if email not in _contributions:
                    _contributions[email] = {"name": contribution["name"], "count": 0}
                _contributions[email]["count"] += contribution["count"]
        return _contributions

    @property
    def file_summaries(self) -> List[FileSummary]:
        if not hasattr(self, "_file_summaries"):
            self._file_summaries = list(
                starmap(
                    lambda filename, line_reports: FileSummary(filename, line_reports),
                    self._blame_reports.items(),
                )
            )
        return self._file_summaries
