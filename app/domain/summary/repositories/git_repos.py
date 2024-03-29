from typing import Iterator, Optional

from config import Settings, get_settings

from ....infrastructure.gitrepo import LocalRepo, RemoteRepo
from ...repos.entities import Repo


class Errors:
    class NoGitRepoFound(Exception):
        pass

    class TooLargeToClone(Exception):
        pass

    class CannotOverwriteLocalRepo(Exception):
        pass


# Maps over local and remote git repo infrastructure
class GitRepo:
    def __init__(self, repo: Repo, config: Settings = get_settings()):
        self._repo = repo
        remote = RemoteRepo(self._repo.git_url)
        self._local = LocalRepo(remote, config.REPOSTORE_PATH)
        self._MAX_SIZE = config.MAX_CLONE_SIZE

    @property
    def local(self) -> LocalRepo:
        if not self.exists_locally:
            raise Errors.NoGitRepoFound
        return self._local

    def delete(self) -> None:
        self._local.delete()

    @property
    def too_large(self) -> bool:
        # A value of zero means there's no limit for cloning
        return self._MAX_SIZE != 0 and self._repo.size > self._MAX_SIZE

    @property
    def exists_locally(self) -> bool:
        return self._local.exists

    def clone(self, verbose=False) -> Optional[Iterator[str]]:
        if self.too_large:
            raise Errors.TooLargeToClone
        if self.exists_locally:
            raise Errors.CannotOverwriteLocalRepo

        if not verbose:
            tuple(self._local.clone_remote())
            return

        yield from self._local.clone_remote()
