import os

os.environ["ENV"] = "test"


from .test_load_all import *

import yaml
import pytest
from vcr import VCR


USERNAME = "ThxSeafood"
REPO_NAME = "thxseafood-app"
API_VER = "/api/v0.1"

CONFIG = get_settings()

with open(os.path.join(WORKDIR, "spec/fixtures/gh_results.yml")) as f:
    CORRECT = yaml.safe_load(f)

CASSETTES_FOLDER = "spec/fixtures/cassettes/"

vcr = VCR(
    record_mode="once",
    path_transformer=VCR.ensure_suffix(".yml"),
    cassette_library_dir=os.path.join(WORKDIR, CASSETTES_FOLDER),
    filter_headers=[("authorization", "<GITHUB_TOKEN>")],
    match_on=["method", "uri", "headers"],
)
