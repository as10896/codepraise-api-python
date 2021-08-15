from fastapi.testclient import TestClient

from .spec_helper import *
from app import app

client = TestClient(app)


from invoke import run

run("inv db.reset -e test")


# HAPPY: should retrieve and store repo and collaborators
@vcr.use_cassette(
    "codepraise_api.posting_to_create_entities_from_github_correct_repo.yml"
)
def test_posting_to_create_entities_from_github_correct_repo():
    response = client.post(f"{API_VER}/repo/{USERNAME}/{REPO_NAME}")
    assert response.status_code == 201
    assert len(response.headers["Location"]) > 0
    repo_data = response.json()
    assert repo_data["size"] > 0


# SAD: should report error if no Github repo found
@vcr.use_cassette("codepraise_api.posting_to_create_entities_from_github_bad_repo.yml")
def test_posting_to_create_entities_from_github_bad_repo():
    response = client.post(f"{API_VER}/repo/{USERNAME}/SAD_REPO_NAME")
    assert response.status_code == 404


# HAPPY: should find stored repo and collaborators
def test_find_stored_repo_and_collaborators_from_db():
    response = client.get(f"{API_VER}/repo/{USERNAME}/{REPO_NAME}")
    assert response.status_code == 200
    repo_data = response.json()
    assert repo_data["size"] > 0


# SAD: should report error if no database repo entity found
def test_find_sad_repo_from_db():
    response = client.get(f"{API_VER}/repo/{USERNAME}/SAD_REPO_NAME")
    assert response.status_code == 404
