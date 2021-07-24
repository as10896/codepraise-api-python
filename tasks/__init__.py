from invoke import Collection

from . import vcr
from . import spec
from . import quality

ns = Collection(spec.spec, quality, vcr)
