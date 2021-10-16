import re
from typing import List, Dict, Optional, Union


# Parses git blame porcelain: https://git-scm.com/docs/git-blame
class Porcelain:

    CODE_LINE_REGEX = r"(\n\t[^\n]*\n)"
    NEWLINE = "\n"

    @classmethod
    def parse_file_blame(
        cls, output: str
    ) -> List[Dict[str, Union[str, Dict[str, str]]]]:
        return list(
            map(
                lambda line: cls.parse_line_blame(line),
                cls.split_by_line_porcelain(output),
            )
        )

    @classmethod
    def split_by_line_porcelain(cls, output: str) -> List[str]:
        try:
            header_code: List[str] = re.split(cls.CODE_LINE_REGEX, output)[:-1]
            header_code: List[str] = [
                "".join(slice) for slice in zip(header_code[::2], header_code[1::2])
            ]
            return header_code
        except:
            raise Exception("blame line parsing failed")

    @classmethod
    def parse_line_blame(cls, porcelain: str) -> Dict[str, Union[str, Dict[str, str]]]:
        line_block: List[str] = porcelain.split(cls.NEWLINE)[:-1]
        line_report = {
            "line_num": cls.parse_first_porcelain(line_block[0]),
            "code": line_block[-1],
        }

        for line in line_block[1:-1]:
            parsed = cls.parse_key_value_porcelain(line)
            if parsed:
                line_report[parsed["key"]] = parsed["value"]

        return line_report

    @classmethod
    def parse_first_porcelain(cls, first_line: str) -> Dict[str, str]:
        elements: List[str] = re.split(r"\s", first_line)
        element_names = ["sha", "linenum_original", "linenum_final", "group_count"]
        return dict(zip(element_names, elements))

    @classmethod
    def parse_key_value_porcelain(cls, line: str) -> Optional[re.Match]:
        return re.match(r"^(?P<key>\S*) (?P<value>.*)", line)
