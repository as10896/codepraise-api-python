from fastapi.testclient import TestClient

from config.environment import SessionLocal

from .spec_helper import *
from application.app import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def db_reset():
    db = SessionLocal()
    db.query(database.orm.CollaboratorORM).delete()
    db.query(database.orm.RepoORM).delete()
    db.query(database.orm.repos_contributors).delete()
    db.commit()
    db.close()


@pytest.fixture
@vcr.use_cassette("codepraise_api/preload_github_correct_repo.yml")
def preload_github_correct_repo():
    from application.services import LoadFromGithub

    db = SessionLocal()
    LoadFromGithub()(db=db, config=CONFIG, ownername=USERNAME, reponame=REPO_NAME)
    db.close()


class TestPostingToCreateEntitiesFromGithub:

    # HAPPY: should retrieve and store repo and collaborators
    @vcr.use_cassette(
        "codepraise_api/posting_to_create_entities_from_github/correct_repo.yml"
    )
    def test_correct_repo(self):
        response = client.post(f"{API_VER}/repo/{USERNAME}/{REPO_NAME}")
        assert response.status_code == 201
        assert len(response.headers["Location"]) > 0
        repo_data = response.json()
        assert repo_data["size"] > 0

    # SAD: should report error if no Github repo found
    @vcr.use_cassette(
        "codepraise_api/posting_to_create_entities_from_github/sad_repo.yml"
    )
    def test_bad_repo(self):
        response = client.post(f"{API_VER}/repo/{USERNAME}/SAD_REPO_NAME")
        assert response.status_code == 400

    # BAD: should report error if duplicate Github repo found
    @vcr.use_cassette(
        "codepraise_api/posting_to_create_entities_from_github/duplicate_repo.yml"
    )
    def test_duplicate_repo(self):
        response = client.post(f"{API_VER}/repo/{USERNAME}/{REPO_NAME}")
        assert response.status_code == 201
        response = client.post(f"{API_VER}/repo/{USERNAME}/{REPO_NAME}")
        assert response.status_code == 409


@pytest.mark.usefixtures("preload_github_correct_repo")
class TestGettingDatabaseEntities:

    # HAPPY: should find stored repo and collaborators
    def test_find_stored_repo_and_collaborators_from_db(self):
        response = client.get(f"{API_VER}/repo/{USERNAME}/{REPO_NAME}")
        assert response.status_code == 200
        repo_data = response.json()
        assert repo_data["size"] > 0

    # SAD: should report error if no database repo entity found
    def test_find_sad_repo_from_db(self):
        response = client.get(f"{API_VER}/repo/{USERNAME}/SAD_REPO_NAME")
        assert response.status_code == 404


@pytest.mark.usefixtures("preload_github_correct_repo")
class TestGettingBlameSummaryPages:

    # HAPPY: should get blame summary for root of loaded repo
    def test_get_blame_summary_for_entire_repo(self):
        response = client.get(f"{API_VER}/summary/{USERNAME}/{REPO_NAME}")
        assert response.status_code == 200
        summary = response.json()
        assert len(summary["base_files"]) == 2
        assert len(summary["subfolders"]) == 6

    # HAPPY should get blame summary for any folder of loaded repo
    def test_get_blame_summary_for_specific_folder(self):
        response = client.get(f"{API_VER}/summary/{USERNAME}/{REPO_NAME}/application")
        assert response.status_code == 200
        summary = response.json()
        assert sorted(summary.keys()) == ["base_files", "folder_name", "subfolders"]
        assert sorted(summary["base_files"].keys()) == ["init.rb"]
        assert sorted(summary["subfolders"].keys()) == [
            "",
            "controllers",
            "representers",
            "services",
            "views",
        ]

    # SAD should report error for repos not loaded
    def test_get_blame_summary_with_sad_repo(self):
        response = client.get(f"{API_VER}/summary/{USERNAME}/bad_repo")
        assert response.status_code == 404

    # SAD should report error for subfolders if repos not loaded
    def test_get_blame_summary_with_sad_repo_for_specific_folder(self):
        response = client.get(f"{API_VER}/summary/{USERNAME}/bad_repo/bad_folder")
        assert response.status_code == 404
