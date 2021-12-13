import re
from typing import List, Optional

from typing_helpers import PorcelainLineReport, PorcelainLineReportLineNum


# Parses git blame porcelain: https://git-scm.com/docs/git-blame
class Porcelain:

    CODE_LINE_REGEX = r"(\n\t[^\n]*\n)"
    NEWLINE = "\n"

    @classmethod
    def parse_file_blame(cls, output: str) -> List[PorcelainLineReport]:
        return list(
            map(
                lambda line: cls.parse_porcelain_line(line),
                cls.split_porcelain_by_line(output),
            )
        )

    @classmethod
    def split_porcelain_by_line(cls, output: str) -> List[str]:
        try:
            header_code: List[str] = re.split(cls.CODE_LINE_REGEX, output)[:-1]
            header_code: List[str] = [
                "".join(slice) for slice in zip(header_code[::2], header_code[1::2])
            ]
            return header_code
        except:
            raise Exception("blame line parsing failed")

    @classmethod
    def parse_porcelain_line(cls, porcelain: str) -> PorcelainLineReport:
        line_block: List[str] = porcelain.split(cls.NEWLINE)[:-1]
        line_report = {
            "line_num": cls.parse_first_porcelain_line(line_block[0]),
            "code": line_block[-1],
        }

        for line in line_block[1:-1]:
            parsed = cls.parse_key_value_porcelain_line(line)
            if parsed:
                line_report[parsed["key"]] = parsed["value"]

        return line_report

    @classmethod
    def parse_first_porcelain_line(cls, first_line: str) -> PorcelainLineReportLineNum:
        elements: List[str] = re.split(r"\s", first_line)
        element_names = ["sha", "linenum_original", "linenum_final", "group_count"]
        return dict(zip(element_names, elements))

    @classmethod
    def parse_key_value_porcelain_line(cls, line: str) -> Optional[re.Match]:
        return re.match(r"^(?P<key>\S*) (?P<value>.*)", line)
