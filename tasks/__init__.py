from invoke import Collection

from . import api, console, db, quality, queue, repostore, spec, vcr, worker

ns = Collection(spec, console, api, worker, vcr, repostore, quality, queue, db)
