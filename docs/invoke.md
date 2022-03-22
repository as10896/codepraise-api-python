# Invoke tasks
Here we use <a href="https://docs.pyinvoke.org/" target="_blank">Invoke</a> as our task management tool.

You can use the container's bash to test these commands.
```shell
docker compose run --rm bash
```

## Commands
```shell
inv -l  # show all tasks
inv [task] -h  # show task help message
inv console -e [env]  # run application console (ipython)
inv test  # run all test scripts (need to run `inv worker.run.test` in another process)
inv api.run -e [env] -p [port]  # run FastAPI server with specified settings (add `-r` or `--reload` to use auto-reload)
inv api.run.dev -p [port]  # rerun FastAPI server in development environment
inv api.run.test -p [port]  # run FastAPI server in test environment
inv api.run.prod -p [port] -h [host] -w [workers]  # run FastAPI server in production environment (with gunicorn)
inv worker.run.dev  # run the background Celery worker in development mode
inv worker.run.prod  # run the background Celery worker in production mode
inv worker.run.test  # run the background Celery worker in test mode
inv queues.create -e [env]  # create SQS queue for Celery
inv queues.purge -e [env]  # purge messages in SQS queue for Celery
inv db.drop -e [env]  # drop all db tables
inv db.migrate -e [env]  # run db schema migrations
inv db.reset -e [env]  # reset all database tables (drop + migrate)
inv db.wipe -e [env]  # delete dev or test sqlite file
inv db.revision  # generate migration script with Alembic (autogeneration with the latest SQLAlchemy models)
inv quality.style  # examine coding style with flake8
inv quality.metric  # measure code metric with radon
inv quality.all  # run all quality tasks (style + metric)
inv quality.reformat  # reformat your code using isort and the black coding style
inv quality.typecheck  # check type with mypy
inv quality  # same as `inv quality.all`
inv repostore.list  # list cloned repos in repo store
inv repostore.create  # create the directory of repostore path
inv repostore.delete  # delete cloned repos in repo store
inv vcr.delete  # delete cassette fixtures (test stubs generated with vcrpy)
```
