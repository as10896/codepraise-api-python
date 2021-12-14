from typing import TypedDict, TypeVar

Filename = TypeVar("Filename", bound=str)
SubfolderName = TypeVar("SubfolderName", bound=str)
ContributorEmail = TypeVar("ContributorEmail", bound=str)

Contribution = TypedDict("Contribution", {"name": str, "count": int})

PorcelainLineReportLineNum = TypedDict(
    "PorcelainLineReportLineNum",
    {"sha": str, "linenum_original": str, "linenum_final": str, "group_count": str},
    total=False,
)

PorcelainLineReport = TypedDict(
    "PorcelainLineReport",
    {
        "line_num": PorcelainLineReportLineNum,
        "code": str,
        "author": str,
        "author-mail": str,
        "author-time": str,
        "author-tz": str,
        "committer": str,
        "committer-mail": str,
        "committer-time": str,
        "committer-tz": str,
        "summary": str,
        "filename": str,
    },
)
