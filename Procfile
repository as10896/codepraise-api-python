release: inv db.migrate -e ${ENV:-development}
web: gunicorn application.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000} --env ENV=${ENV:-development}
worker: ENV=${ENV:-development} celery --app=workers.clone_repo_worker:celery worker --loglevel=INFO