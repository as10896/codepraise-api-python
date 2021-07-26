from .spec_helper import *


vcr = VCR(
    record_mode="once",
    path_transformer=VCR.ensure_suffix(".yml"),
    cassette_library_dir=os.path.join(WORKDIR, CASSETTES_FOLDER),
    filter_headers=[
        "authorization"
    ],  # filter sensitive information (GitHub API token) from HTTP response
    match_on=["method", "uri", "headers"],
)


@pytest.fixture(scope="module")
@vcr.use_cassette("github_api.correct_repo.yml")
def repo():
    return GithubAPI(GH_TOKEN).repo(USERNAME, REPO_NAME)


class TestGithubAPI:
    @vcr.use_cassette("github_api.test_repo.yml")
    def test_repo(self, repo):
        # HAPPY: should provide correct repo attributes
        assert repo.size == CORRECT["size"]
        assert repo.git_url == CORRECT["git_url"]

        # SAD: should raise exception on incorrect repo
        with pytest.raises(Errors.NotFound):
            GithubAPI(GH_TOKEN).repo("allenai", "foobar")

        # SAD: should raise exception when unauthorized
        with pytest.raises(Errors.Unauthorized):
            GithubAPI("BAD_TOKEN").repo(USERNAME, REPO_NAME)

    # Contributor information
    @vcr.use_cassette("github_api.test_contributors.yml")
    def test_contributors(self, repo):

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
