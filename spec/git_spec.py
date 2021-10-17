from .spec_helper import *


@pytest.fixture
@vcr.use_cassette("codepraise_api/preload_github_correct_repo.yml")
def repo():
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


# HAPPY: should get blame summary for a remote repo
def test_git_commands_mapper_and_gateway(repo):
    summary = blame_reporter.Summary(repo)
    full_repo_summary = summary.for_folder("")
    assert len(full_repo_summary.contributions) == 3

    first_collab = full_repo_summary.contributions["<soumya.ray@gmail.com>"]
    assert first_collab["count"] == 433
    assert first_collab["name"] == "Soumya Ray"
