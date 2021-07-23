import yaml
import os
import sys
import pytest

WORKDIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(WORKDIR)

from lib.github_api import GithubAPI
from lib.contributor import Contributor


USERNAME = "allenai"
REPO_NAME = "science-parse"

with open(os.path.join(WORKDIR, "config/secrets.yml")) as f:
    CONFIG = yaml.safe_load(f)

GH_TOKEN = CONFIG['gh_token']

with open(os.path.join(WORKDIR, "spec/fixtures/gh_results.yml")) as f:
    CORRECT = yaml.safe_load(f)

with open(os.path.join(WORKDIR, "spec/fixtures/gh_response.yml")) as f:
    RESPONSE = yaml.load(f, Loader=yaml.Loader)


# Repo information
def test_repo():

    # HAPPY: should provide correct repo attributes
    repo = GithubAPI(GH_TOKEN, cache=RESPONSE).repo(USERNAME, REPO_NAME)
    assert repo.size == CORRECT["size"]
    assert repo.git_url == CORRECT["git_url"]

    # SAD: should raise exception on incorrect repo
    with pytest.raises(GithubAPI.Errors.NotFound):
        GithubAPI(GH_TOKEN, cache=RESPONSE).repo("allenai", "foobar")


# Contributor information
def test_contributors():
    repo = GithubAPI(GH_TOKEN, cache=RESPONSE).repo(USERNAME, REPO_NAME)

    # HAPPY: should recognize owner
    assert isinstance(repo.owner, Contributor)

    # HAPPY: should identify owner
    assert repo.owner.username is not None
    assert repo.owner.username == CORRECT["owner"]["login"]

    # HAPPY: should identify contributors
    contributors = repo.contributors
    assert len(contributors) == len(CORRECT['contributors'])

    usernames = list(map(lambda c: c.username, contributors))
    correct_usernames = list(map(lambda c: c["login"], CORRECT["contributors"]))
    assert usernames == correct_usernames
