from .spec_helper import *


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "record_mode": "once",
        "cassette_library_dir": os.path.join(WORKDIR, CASSETTES_FOLDER),
        "path_transformer": vcr.VCR.ensure_suffix(".yml"),
        "filter_headers": [
            "authorization"
        ],  # filter sensitive information (GitHub API token) from HTTP response
    }


@pytest.mark.vcr
class TestGithubAPI:
    def test_repo(self):
        # HAPPY: should provide correct repo attributes
        repo = GithubAPI(GH_TOKEN).repo(USERNAME, REPO_NAME)
        assert repo.size == CORRECT["size"]
        assert repo.git_url == CORRECT["git_url"]

        # SAD: should raise exception on incorrect repo
        with pytest.raises(Errors.NotFound):
            GithubAPI(GH_TOKEN).repo("allenai", "foobar")

        # SAD: should raise exception when unauthorized
        with pytest.raises(Errors.Unauthorized):
            GithubAPI("BAD_TOKEN").repo("allenai", "foobar")

    # Contributor information
    def test_contributors(self):
        repo = GithubAPI(GH_TOKEN).repo(USERNAME, REPO_NAME)

        # HAPPY: should recognize owner
        assert isinstance(repo.owner, Contributor)

        # HAPPY: should identify owner
        assert repo.owner.username is not None
        assert repo.owner.username == CORRECT["owner"]["login"]

        # HAPPY: should identify contributors
        contributors = repo.contributors
        assert len(contributors) == len(CORRECT["contributors"])

        usernames = list(map(lambda c: c.username, contributors))
        correct_usernames = list(map(lambda c: c["login"], CORRECT["contributors"]))
        assert usernames == correct_usernames
