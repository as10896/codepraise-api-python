from typing import List, Dict, Union

from infrastructure import gitrepo
from domain import entities
from config import Settings, get_settings
from .porcelain_parser import Porcelain


# Produces blame report for an entire remote repo
class Summary:
    DEFAULT_EXCLUDE_FOLDERS = ["fixtures"]

    def __init__(self, repo: entities.Repo, config: Settings = get_settings()):
        origin = gitrepo.RemoteRepo(repo.git_url)
        self._local = gitrepo.LocalRepo(origin, config.repostore_path)
        self._blame_reports = Report(self._local)

    def for_folder(self, folder_name: str) -> entities.FolderSummary:
        reports = self._blame_reports.in_folder(folder_name)
        return entities.FolderSummary(folder_name, reports)


# Git blame related services
class Report:
    def __init__(self, local_gitrepo: gitrepo.LocalRepo):
        self._local = local_gitrepo

    def in_folder(
        self, folder_name: str
    ) -> Dict[str, List[Dict[str, Union[str, Dict[str, str]]]]]:
        files = filter(lambda file: file.startswith(folder_name), self._local.files)
        with self._local.in_repo():
            return dict(
                map(lambda filename: [filename, self._report_for_file(filename)], files)
            )

    @classmethod
    def _report_for_file(
        cls, filename: str
    ) -> List[Dict[str, Union[str, Dict[str, str]]]]:
        blame_output: str = gitrepo.RepoFile(filename).blame
        return Porcelain.parse_file_blame(blame_output)
