from fastapi.testclient import TestClient

from .spec_helper import *
from main import app

client = TestClient(app)


# HAPPY: should provide correct repo attributes
@vcr.use_cassette("codepraise_api.correct_repo.yml")
def test_correct_repo():
    response = client.get(f"{API_VER}/repo/{USERNAME}/{REPO_NAME}")
    assert response.status_code == 200
    repo_data = response.json()
    assert repo_data["repo"]["size"] > 0


# SAD: should raise exception on incorrect repo
@vcr.use_cassette("codepraise_api.incorrect_repo.yml")
def test_incorrect_repo():
    response = client.get(f"{API_VER}/repo/{USERNAME}/bad_repo")
    assert response.status_code == 404
    repo_data = response.json()
    assert repo_data["detail"] == {"error": "Repo not found"}
