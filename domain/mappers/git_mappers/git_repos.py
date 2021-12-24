from typing import Iterator, Optional

from config import Settings, get_settings
from infrastructure.gitrepo import LocalRepo, RemoteRepo

from ...entities import Repo


class Errors:
    class NoGitRepoFound(Exception):
        pass

    class TooLargeToClone(Exception):
        pass

    class CannotOverwriteLocalRepo(Exception):
        pass


# Maps over local and remote git repo infrastructure
class GitRepo:

    _MAX_SIZE = 1000  # for cloning, analysis, summaries, etc.

    def __init__(self, repo: Repo, config: Settings = get_settings()):
        self._repo = repo
        remote = RemoteRepo(self._repo.git_url)
        self._local = LocalRepo(remote, config.REPOSTORE_PATH)

    @property
    def local(self) -> LocalRepo:
        if not self.exists_locally:
            raise Errors.NoGitRepoFound
        return self._local

    def delete(self) -> None:
        self._local.delete()

    @property
    def too_large(self) -> bool:
        self._repo.size > self._MAX_SIZE

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
