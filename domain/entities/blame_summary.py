from typing import Dict, List, Union
from itertools import starmap

from infrastructure import gitrepo
from ..blame_reporter import Report


# Produces blame report for an entire remote repo
# TODO: exclude folders feature, refactor, file counts
class BlameSummary:

    DEFAULT_EXCLUDE_FOLDERS = ["fixtures"]

    def __init__(self, local_repo: gitrepo.LocalRepo):
        self._local = local_repo

    @property
    def local(self) -> gitrepo.LocalRepo:
        return self._local

    def summarize_folder(
        self, folder_name: str
    ) -> Dict[str, Union[str, Dict[str, Dict[str, Union[int, str]]]]]:
        relevant_file_summaries = filter(
            lambda summary: summary["filename"].startswith(folder_name),
            self.file_summaries,
        )

        contributions = {}
        for summary in relevant_file_summaries:
            for email, contribution in summary["contributions"].items():
                if email not in contributions:
                    contributions[email] = {"name": contribution["name"], "count": 0}
                contributions[email]["count"] += contribution["count"]

        return {"folder_name": folder_name, "contributions": contributions}

    @property
    def file_summaries(
        self,
    ) -> List[Dict[str, Union[str, Dict[str, Dict[str, Union[int, str]]]]]]:
        if hasattr(self, "_file_summaries"):
            return self._file_summaries

        file_reports = self._blame_all_files
        self._file_summaries = list(
            starmap(
                lambda filename, line_reports: self._summarize_file_report(
                    filename, line_reports
                ),
                file_reports.items(),
            )
        )

        return self._file_summaries

    def _summarize_file_report(
        self, filename: str, line_reports: List[Dict[str, Union[str, Dict[str, str]]]]
    ) -> Dict[str, Union[str, Dict[str, Dict[str, Union[int, str]]]]]:
        contributions = {}

        for report in line_reports:
            if report["author-mail"] not in contributions:
                contributions[report["author-mail"]] = {
                    "name": report["author"],
                    "count": 0,
                }
            contributions[report["author-mail"]]["count"] += 1

        return {"filename": filename, "contributions": contributions}

    @property
    def _blame_all_files(
        self,
    ) -> Dict[str, List[Dict[str, Union[str, Dict[str, str]]]]]:
        files = self._local.files
        with self._local.in_repo():
            files = dict(
                map(lambda filename: [filename, Report.for_file(filename)], files)
            )

        return files
