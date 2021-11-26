from typing import List, Dict, Union

from infrastructure import gitrepo
from config import Settings, get_settings
from .porcelain_parser import Porcelain
from ..entities import Repo


# Git blame parsing and reporting services
class Reporter:
    def __init__(self, repo: Repo, config: Settings = get_settings()):
        origin = gitrepo.RemoteRepo(repo.git_url)
        self._local = gitrepo.LocalRepo(origin, config.REPOSTORE_PATH)

    def folder_report(
        self, folder_name: str
    ) -> Dict[str, List[Dict[str, Union[str, Dict[str, str]]]]]:
        if folder_name == "/":
            folder_name = ""

        files = filter(lambda file: file.startswith(folder_name), self._local.files)
        with self._local.in_repo():
            return dict(
                map(lambda filename: [filename, self.file_report(filename)], files)
            )

    @property
    def files(self, folder_name: str) -> List[str]:
        return list(
            filter(lambda file: file.startswith(folder_name), self._local.files)
        )

    @property
    def subfolders(self, folder_name: str) -> List[str]:
        return self._local.folder_structure[folder_name]

    @property
    def folder_structure(self) -> Dict[str, List[str]]:
        return self._local.folder_structure

    @classmethod
    def file_report(cls, filename: str) -> List[Dict[str, Union[str, Dict[str, str]]]]:
        blame_output: str = gitrepo.RepoFile(filename).blame
        return Porcelain.parse_file_blame(blame_output)
