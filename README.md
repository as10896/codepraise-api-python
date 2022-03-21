# codepraise-api-python
[![CI](https://github.com/as10896/codepraise-api-python/actions/workflows/ci.yml/badge.svg)](https://github.com/as10896/codepraise-api-python/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/as10896/codepraise-api-python/branch/main/graph/badge.svg?token=ZFX6A4M0XX)](https://codecov.io/gh/as10896/codepraise-api-python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

This is a Python reproduction of [ISS-SOA/codepraise-api](https://github.com/ISS-SOA/codepraise-api), a demo project for NTHU Service-Oriented Architecture course (for practice only).

For Web client / Notifier, please visit [codepraise-app-python](https://github.com/as10896/codepraise-app-python) / [codepraise-clone-notifier-python](https://github.com/as10896/codepraise-clone-notifier-python).

## Prerequisite
### Install Docker
Make sure you have the latest version of [Docker 🐳](https://www.docker.com/get-started) installed on your local machine.

### Secrets setup
Placing secret values in files is a common pattern to provide sensitive configuration to an application. A secret file follows the same principal as a `.env` file except it only contains a single value and the file name is used as the key.

A secret file will look like the following:

`/var/run/database_password`:

```
super_secret_database_password
```

Here we create secret files under the secret directories (`config/secrets/<env>/`) and place secret values into the files.

You can also set up environment variables directly.\
The variables you set in this way would take precedence over those loaded from a secret file.

For more info, check the [pydantic official document](https://pydantic-docs.helpmanual.io/usage/settings/#secret-support).

#### Create GitHub API personal access token
1. Generate token [here](https://github.com/settings/tokens).
2. Create `GH_TOKEN` under `config/secrets/<env>/` with the generated token (or just setting the environment variable `GH_TOKEN`).

#### Set up Amazon SQS
1. Create an AWS account and an IAM user ([Ref](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-setting-up.html)).
2. Create `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` under `config/secrets/<env>/` with the generated credentials (or just setting environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`).
3. Select a region where FIFO Queues are available (e.g. `us-east-1`, see [here](https://aws.amazon.com/about-aws/whats-new/2019/02/amazon-sqs-fifo-qeues-now-available-in-15-aws-regions/) for more info), then creating `AWS_REGION` under `config/secrets/<env>/` with the region name (or just setting the environment variable `AWS_REGION`).
4. Create a **FIFO** Amazon SQS queue ([Ref](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-create-queue.html)).
    * Notice that the name of a FIFO queue must end with the `.fifo` suffix.
5. Create `CLONE_QUEUE` under `config/secrets/<env>/` with the created queue's name (or just setting the environment variable `CLONE_QUEUE`).
6. Create another FIFO Amazon SQS queue, and then create `REPORT_QUEUE` under `config/secrets/<env>/` with the created queue's name  (or just setting the environment variable `REPORT_QUEUE`).
    * Not needed for test environment.

## Run with Docker
You can start all the services easily with Docker Compose.\
Before starting, make sure you have all the configurations set up as mentioned above.

For convenience, you can use a `.env` file with all the necessary variables configured as follows:

```shell
export GH_TOKEN=<github credentials>
export AWS_ACCESS_KEY_ID=<aws credentials>
export AWS_SECRET_ACCESS_KEY=<aws credentials>
export AWS_REGION=<aws credentials>
export CLONE_QUEUE=<aws sqs queue>
export REPORT_QUEUE=<aws sqs queue>
```

Then `source` the configuration file:

```shell
source .env
```

Notice that it is not recommended to `export` all these credentials directly in the shell since these will be logged into shell history if not inserted through secure input.\
Don't do that especially when you're using a shared device that might be accessed by multiple users.

### Development
Uvicorn + Celery + SQLite + In-memory Pub/Sub
```shell
docker compose up -d  # run services in the background
docker compose run --rm console  # run application console with database connected
docker compose down  # shut down all the services
```
After starting, you can visit http://localhost:8000/docs to see the interactive API documentation.

### Production
Gunicorn + Uvicorn + Celery + PostgreSQL + Redis Pub/Sub
```shell
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d  # run services in the background
docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm console  # run application console with database connected
docker compose -f docker-compose.yml -f docker-compose.prod.yml down  # shut down all the services
docker compose -f docker-compose.yml -f docker-compose.prod.yml down -v  # shut down all the services and remove all the volumes
```
After starting, you can visit http://localhost:8000/docs to see the interactive API documentation.

### Testing
```shell
docker compose -f docker-compose.test.yml run --rm test  # run TDD tests
docker compose -f docker-compose.test.yml --profile bdd up -d  # run services for the usage of frontend BDD testing
docker compose -f docker-compose.test.yml --profile bdd down  # shut down all the services for BDD testing
```


## Invoke tasks
Here we use [invoke](https://docs.pyinvoke.org/) as our task management tool.

You can use the container's bash to test these commands.
```shell
docker compose run --rm bash
```

### Commands
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
