release: inv db.migrate -e production
web: inv worker.run.prod & inv api.run.prod -p ${PORT:-8000}