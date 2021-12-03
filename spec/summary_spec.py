from .spec_helper import *


@pytest.fixture
@vcr.use_cassette("codepraise_api/preload_github_correct_repo.yml")
def repo() -> entities.Repo:
    from config.environment import SessionLocal
    from application.services import LoadFromGithub

    db = SessionLocal()
    db.query(database.orm.CollaboratorORM).delete()
    db.query(database.orm.RepoORM).delete()
    db.query(database.orm.repos_contributors).delete()
    db.commit()

    LoadFromGithub()(db=db, config=CONFIG, ownername=USERNAME, reponame=REPO_NAME)
    _repo = repository.CRUDRepo.find_full_name(db, USERNAME, REPO_NAME)
    db.close()

    return _repo


# HAPPY: should get blame summary for entire repo
@pytest.mark.asyncio
async def test_blame_summary_for_entire_repo(repo: entities.Repo):
    summary = await blame_reporter.Summary(repo).for_folder("")

    assert len(summary.subfolders) == 6
    assert len(summary.base_files) == 2
    assert sorted(summary.base_files.keys())[0] == "README.md"
    assert sorted(summary.subfolders.keys())[0] == ""


# HAPPY: should get accurate blame summary for specific folder
@pytest.mark.asyncio
async def test_blame_summary_for_specific_folder(repo: entities.Repo):
    summary = await blame_reporter.Summary(repo).for_folder("application")

    assert len(summary.subfolders) == 5
    assert summary.subfolders["views"]["<as10896@gmail.com>"] == {
        "name": "as10896",
        "count": 197,
    }
    assert summary.subfolders["views"]["<kenlyx1124@g.ncu.edu.tw>"] == {
        "name": "kenlyx",
        "count": 47,
    }

    assert len(summary.base_files) == 1
    assert summary.base_files["init.rb"]["<as10896@gmail.com>"] == {
        "name": "as10896",
        "count": 6,
    }