# codepraise-api-python
[![Test](https://github.com/as10896/codepraise-api-python/actions/workflows/test.yml/badge.svg)](https://github.com/as10896/codepraise-api-python/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/as10896/codepraise-api-python/branch/main/graph/badge.svg?token=ZFX6A4M0XX)](https://codecov.io/gh/as10896/codepraise-api-python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## Prerequisite
### Create virtual environment
Here we use [Pipenv](https://pipenv.pypa.io/en/latest/) to create our virtual environment.

```bash
pip install pipenv  # install pipenv
pipenv --python 3.9  # create Python 3.9 virtualenv under current directory
pipenv shell  # activate the virtualenv of the current directory
pipenv install --dev  # install required dependencies with Pipfile
```

### Create GitHub API personal access token
1. Generate token [here](https://github.com/settings/tokens)
2. Create `GH_TOKEN` under `config/secrets/<env>/` with the generated token

### Set up Amazon SQS
1. Create an AWS account and an IAM user ([Ref](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-setting-up.html)).
2. Create `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` under `config/secrets/<env>/` with the generated credentials.
3. Select a region where FIFO Queues are available (e.g. `us-east-1`, see [here](https://aws.amazon.com/about-aws/whats-new/2019/02/amazon-sqs-fifo-qeues-now-available-in-15-aws-regions/) for more info), then creating `AWS_REGION` under `config/secrets/<env>/` with the region name.
3. Create a **FIFO** Amazon SQS queue ([Ref](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-create-queue.html)).
    * Notice that the name of a FIFO queue must end with the `.fifo` suffix.
4. Create `CLONE_QUEUE` under `config/secrets/<env>/` with the created queue's name.
5. Create another FIFO Amazon SQS queue, and then create `REPORT_QUEUE` under `config/secrets/<env>/` with the created queue's name (not needed for test environment).

## CLI usage
Here we use [invoke](https://docs.pyinvoke.org/) as our task management tool

```bash
inv -l  # show all tasks
inv [task] -h  # show task help message
inv console  # run application console (ipython)
inv spec  # run all test scripts (need to run `inv worker.run.test` in another process)
inv api.run -m [mode] -p [port]  # run FastAPI server with specified settings (add `-r` or `--reload` to use auto-reload)
inv api.run.dev -p [port]  # rerun FastAPI server in development environment
inv api.run.test -p [port]  # run FastAPI server in test environment
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
