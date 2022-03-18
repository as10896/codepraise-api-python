from invoke import Collection

from . import api, console, db, quality, queues, repostore, test, vcr, worker

ns = Collection(test, console, api, worker, vcr, repostore, quality, queues, db)
