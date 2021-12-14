release: inv db.migrate
web: inv worker.run.prod & gunicorn application.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}