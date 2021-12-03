from invoke import Collection

from . import vcr
from . import spec
from . import quality
from . import api
from . import console
from . import db
from . import repostore


ns = Collection(spec.spec, quality, vcr.rmvcr, api, console.console, db, repostore)
