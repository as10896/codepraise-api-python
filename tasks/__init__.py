from invoke import Collection

from . import spec
from . import console
from . import api
from . import worker
from . import vcr
from . import repostore
from . import quality
from . import queue
from . import db


ns = Collection(spec, console, api, worker, vcr, repostore, quality, queue, db)
