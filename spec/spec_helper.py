import yaml
import os
import sys
import pytest
import vcr

WORKDIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(WORKDIR)

from lib.github_api import GithubAPI, Errors
from lib.contributor import Contributor

USERNAME = "allenai"
REPO_NAME = "science-parse"

with open(os.path.join(WORKDIR, "config/secrets.yml")) as f:
    CONFIG = yaml.safe_load(f)

GH_TOKEN = CONFIG['gh_token']

with open(os.path.join(WORKDIR, "spec/fixtures/gh_results.yml")) as f:
    CORRECT = yaml.safe_load(f)

CASSETTES_FOLDER = "spec/fixtures/cassettes/"
