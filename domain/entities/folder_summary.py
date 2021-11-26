import re
from typing import Dict, List, Union
from itertools import starmap

from .file_summary import FileSummary
from ..blame_reporter import Reporter


# Summarizes blame reports for an entire folder
class FolderSummary:
    def __init__(self, git_url: str, folder_name: str):
        self._folder_name = folder_name
        self._blame_reports: Dict[
            str, List[Dict[str, Union[str, Dict[str, str]]]]
        ] = Reporter(git_url).folder_report(folder_name)

    @property
    def folder_name(self) -> str:
        return self._folder_name

    @property
    def subfolders(self) -> Dict[str, Dict[str, Dict[str, Union[int, str]]]]:
        structured: Dict[str, List[FileSummary]] = {}
        for filename, file_summary in self.file_summaries.items():
            subfolder: str = self._rel_path(filename)
            structured.setdefault(subfolder, []).append(file_summary)

        return dict(
            starmap(
                lambda subfolder, subfolder_summaries: [
                    subfolder,
                    self._add_contributions(subfolder_summaries),
                ],
                structured.items(),
            )
        )

    @property
    def base_files(self) -> Dict[str, Dict[str, Dict[str, Union[int, str]]]]:
        return dict(
            starmap(
                lambda filename, summary: [
                    self._filename_only(filename),
                    summary.contributions,
                ],
                filter(
                    lambda file_summary: self._base_level_file(file_summary[0]),
                    self.file_summaries.items(),
                ),
            )
        )

    def _base_level_file(self, filename: str) -> bool:
        return len(self._rel_path(filename)) == 0

    def _add_contributions(
        self, summaries: List[FileSummary]
    ) -> Dict[str, Dict[str, Union[int, str]]]:
        contributions = {}
        for summary in summaries:
            for email, contribution in summary.contributions.items():
                if email not in contributions:
                    contributions[email] = {
                        "name": contribution["name"],
                        "count": 0,
                    }
                contributions[email]["count"] += contribution["count"]

        return contributions

    @property
    def file_summaries(self) -> Dict[str, FileSummary]:
        if not hasattr(self, "_file_summaries"):
            self._file_summaries = starmap(
                lambda filename, line_reports: FileSummary(filename, line_reports),
                self._blame_reports.items(),
            )
            self._file_summaries = {
                summary.filename: summary for summary in self._file_summaries
            }
        return self._file_summaries

    @property
    def folder_prefix_length(self) -> int:
        if not hasattr(self, "_folder_prefix_length"):
            self._folder_prefix_length = (
                0 if len(self.folder_name) == 0 else len(self.folder_name) + 1
            )
        return self._folder_prefix_length

    def _rel_path(self, filename: str) -> str:
        rel_filename = filename[self.folder_prefix_length :]
        match = re.match(r"(?P<folder>[^/]+)/.*", rel_filename)
        return match["folder"] if match else ""

    def _filename_only(self, filename: str) -> str:
        rel_filename = filename[self.folder_prefix_length :]
        match = re.match(r"(?P<subfolder>.*/)?(?P<file>.*)", rel_filename)
        return match["file"]
