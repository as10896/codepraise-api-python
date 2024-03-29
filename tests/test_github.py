from .helper import *


@pytest.fixture(scope="module")
@vcr.use_cassette("github_api/correct_repo.yml")
def repo() -> repo_entities.Repo:
    repo_mapper = repo_mappers.RepoMapper(CONFIG)
    return repo_mapper.find(USERNAME, REPO_NAME)


class TestRepo:

    # HAPPY: should provide correct repo attributes
    def test_correct_repo(self, repo):
        assert repo.size == CORRECT["size"]
        assert repo.git_url == CORRECT["git_url"]

    # SAD: should raise exception on incorrect repo
    @vcr.use_cassette("github_api/incorrect_repo.yml")
    def test_incorrect_repo(self):
        repo_mapper = repo_mappers.RepoMapper(CONFIG)
        with pytest.raises(github.API.Errors.NotFound):
            repo = repo_mapper.find(USERNAME, "SAD_REPO_NAME")

    # SAD: should raise exception when unauthorized
    @vcr.use_cassette("github_api/invalid_token.yml")
    def test_invalid_token(self):
        SAD_CONFIG = get_settings(GH_TOKEN="sad_token")
        repo_mapper = repo_mappers.RepoMapper(SAD_CONFIG)
        with pytest.raises(github.API.Errors.Unauthorized):
            repo = repo_mapper.find(USERNAME, REPO_NAME)


class TestContributor:

    # HAPPY: should recognize owner
    def test_owner_class(self, repo):
        assert isinstance(repo.owner, repo_entities.Collaborator)

    # HAPPY: should identify owner
    def test_owner_info(self, repo):
        assert repo.owner.username is not None
        assert repo.owner.username == CORRECT["owner"]["login"]

    # HAPPY: should identify contributors
    def test_contributors(self, repo):
        contributors = repo.contributors
        assert len(contributors) == len(CORRECT["contributors"])

        usernames = list(map(lambda c: c.username, contributors))
        correct_usernames = list(map(lambda c: c["login"], CORRECT["contributors"]))
        assert usernames == correct_usernames
