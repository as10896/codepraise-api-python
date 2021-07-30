import os
import sys

WORKDIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(WORKDIR)

from config import config
from lib.github.api import API
from lib.github.mappers.repo_mapper import RepoMapper
from lib.entities.contributor import Contributor
