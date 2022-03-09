release: inv db.migrate
web: inv worker.run.prod & inv api.run.prod -p ${PORT:-8000}