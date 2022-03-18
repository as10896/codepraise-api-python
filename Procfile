release: inv db.migrate -e production
web: inv worker.run.prod -p 2 & inv api.run.prod -p ${PORT:-8000} -w 2