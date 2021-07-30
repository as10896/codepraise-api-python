from invoke import Collection

from . import vcr
from . import spec
from . import quality
from . import api

ns = Collection(spec.spec, quality, vcr.rmvcr, api)
