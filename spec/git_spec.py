from .spec_helper import *


@pytest.fixture
def local_repo():
    git_url = "git://github.com/allenai/science-parse.git"
    origin = gitrepo.RemoteRepo(git_url)
    _local_repo = gitrepo.LocalRepo(origin, CONFIG.repostore_path)
    if not _local_repo.exists:
        _local_repo.clone_remote()
    return _local_repo


# HAPPY: should get blame summary for a remote repo
def test_git_commands_mapper_and_gateway(local_repo):
    report = entities.BlameSummary(local_repo)
    report.summarize_folder("")
