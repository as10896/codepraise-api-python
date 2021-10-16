import os
import re
import glob
import base64
import hashlib
import shutil
import subprocess
from contextlib import contextmanager
from typing import List, Dict, Generator


class Errors:
    class InvalidLocalRepo(Exception):
        pass


# Manage remote Git repository for cloning
class RemoteRepo:
    def __init__(self, git_url: str):
        self._git_url = git_url

    def local_clone(self, path: str) -> None:
        cmd = f"git clone {self._git_url} {path}"
        subprocess.run(cmd.split(), check=True)

    @property
    def unique_id(self) -> str:
        digest: bytes = hashlib.sha256(self._git_url.encode()).digest()
        return base64.urlsafe_b64encode(digest).decode()

    @property
    def git_url(self) -> str:
        return self._git_url


# Manage local Git repository
class LocalRepo:

    ONLY_FOLDERS = "**/"
    FILES_AND_FOLDERS = "**/*"
    CODE_FILENAME_MATCH = r".(py|js|ts|vue|rb|go|java|c|cpp|php|sh|html|css|scss|json|yml|yaml|xml|txt|csv|tsv|md|ini)$"

    def __init__(self, remote: RemoteRepo, repostore_path: str):
        self._remote = remote
        self._repo_path = "/".join([repostore_path, self._remote.unique_id])
        if not self.exists:
            self.clone_remote()

    def clone_remote(self) -> None:
        self._remote.local_clone(self._repo_path)

    @property
    def repo_path(self) -> str:
        return self._repo_path

    @property
    def folder_structure(self) -> Dict[str, List[str]]:
        self._raise_unless_setup()
        if hasattr(self, "_folder_structure"):
            return self._folder_structure

        self._folder_structure = {"/": []}

        with self.in_repo():
            all_folders = glob.glob(self.ONLY_FOLDERS, recursive=True)
            for full_path in all_folders:
                parts = full_path.split("/")
                parent = "/" if len(parts) == 2 else "/".join(parts[:-2])
                if parent not in self._folder_structure:
                    self._folder_structure[parent] = []
                self._folder_structure[parent].append(full_path)

        return self._folder_structure

    @property
    def files(self) -> List[str]:
        self._raise_unless_setup()
        if hasattr(self, "_files"):
            return self._files

        with self.in_repo():
            self._files = list(
                filter(
                    lambda path: os.path.isfile(path)
                    and re.findall(self.CODE_FILENAME_MATCH, path),
                    glob.glob(self.FILES_AND_FOLDERS, recursive=True),
                )
            )
        return self._files

    @contextmanager
    def in_repo(self) -> Generator:
        self._raise_unless_setup()
        old_cwd = os.getcwd()
        os.chdir(self._repo_path)
        yield
        os.chdir(old_cwd)

    @property
    def exists(self) -> bool:
        return os.path.exists(self._repo_path)

    def _raise_unless_setup(self) -> None:
        if not self.exists:
            raise Errors.InvalidLocalRepo

    def _wipe(self) -> None:
        shutil.rmtree(self._repo_path)
