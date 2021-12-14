from typing import Dict, List

from typing_helpers import Contribution, ContributorEmail, PorcelainLineReport


# Summarizes a single file's blame report
class FileSummary:
    def __init__(self, filename: str, line_reports: List[PorcelainLineReport]):
        self._filename = filename
        self._line_reports = line_reports

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def contributions(self) -> Dict[ContributorEmail, Contribution]:
        if not hasattr(self, "_contributions"):
            self._contributions = self._summarize_line_reports(self._line_reports)
        return self._contributions

    def _summarize_line_reports(
        self, line_reports: List[PorcelainLineReport]
    ) -> Dict[ContributorEmail, Contribution]:
        contributions = {}
        for report in line_reports:
            if report["author-mail"] not in contributions:
                contributions[report["author-mail"]] = {
                    "name": report["author"],
                    "count": 0,
                }
            contributions[report["author-mail"]]["count"] += 1
        return contributions
