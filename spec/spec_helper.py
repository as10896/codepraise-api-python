import os

os.environ["ENV"] = "test"


import pytest
import yaml
from vcr import VCR

from app.application.app import app

from .test_load_all import *

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
    ignore_hosts=[f"sqs.{CONFIG.AWS_REGION}.amazonaws.com"],
    filter_headers=[("authorization", "<GITHUB_TOKEN>")],
    match_on=["method", "uri", "headers"],
)
