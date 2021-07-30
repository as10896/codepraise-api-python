from .test_load_all import *

import yaml
import pytest
from vcr import VCR


USERNAME = "allenai"
REPO_NAME = "science-parse"
API_VER = "/api/v0.1"

CONFIG = config.get_settings(mode="test")
GH_TOKEN = CONFIG.gh_token

with open(os.path.join(WORKDIR, "spec/fixtures/gh_results.yml")) as f:
    CORRECT = yaml.safe_load(f)

CASSETTES_FOLDER = "spec/fixtures/cassettes/"

vcr = VCR(
    record_mode="once",
    path_transformer=VCR.ensure_suffix(".yml"),
    cassette_library_dir=os.path.join(WORKDIR, CASSETTES_FOLDER),
    filter_headers=["authorization"],
    match_on=["method", "uri", "headers"],
)
