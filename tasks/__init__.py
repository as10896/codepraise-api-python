from invoke import Collection

from . import vcr
from . import spec
from . import quality
from . import api
from . import console
from . import db


ns = Collection(spec, quality, vcr.rmvcr, api, console.console, db)
