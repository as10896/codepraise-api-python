from typing import List, Dict, Union

from infrastructure import gitrepo
from .porcelain_parser import Porcelain


class Report:
    @classmethod
    def for_file(cls, filename: str) -> List[Dict[str, Union[str, Dict[str, str]]]]:
        blame_output: str = gitrepo.RepoFile(filename).blame
        return Porcelain.parse_file_blame(blame_output)
