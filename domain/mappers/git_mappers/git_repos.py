from ...entities import Repo
from config import Settings, get_settings
from infrastructure.gitrepo import RemoteRepo, LocalRepo


class Errors:
    class NoGitRepoFound(Exception):
        pass

    class TooLargeToClone(Exception):
        pass

    class CannotOverwriteLocalRepo(Exception):
        pass


class GitRepo:

    _MAX_SIZE = 1000  # for cloning, analysis, summaries, etc.

    def __init__(self, repo: Repo, config: Settings = get_settings()):
        self._repo = repo
        origin = RemoteRepo(self._repo.git_url)
        self._local = LocalRepo(origin, config.REPOSTORE_PATH)

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

    def clone(self) -> None:
        if self.too_large:
            raise Errors.TooLargeToClone
        if self.exists_locally:
            raise Errors.CannotOverwriteLocalRepo

        self._local.clone_remote()
