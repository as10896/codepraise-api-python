# codepraise-api-python
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Prerequisite
### Create virtual environment
Here we use [Pipenv](https://pipenv.pypa.io/en/latest/) to create our virtual environment.

```bash
pip install pipenv  # install pipenv
pipenv --three  # create Python 3 virtualenv under current directory
pipenv shell  # activate the virtualenv of the current directory
pipenv install --dev  # install required dependencies with Pipfile (or Pipfile.lock, if any)
```

### Create GitHub API personal access token
1. Generate token [here](https://github.com/settings/tokens)
2. Create `gh_token` under `config/secrets/<env>/` with the generated token


## Usage
Here we use [invoke](https://docs.pyinvoke.org/) as our task management tool

```bash
inv -l  # show all tasks
inv [task] -h  # show task help message
inv console  # run console
inv spec  # run all test scripts
inv spec.type  # check type with mypy
inv api.run -m [mode] -p [port]  # rerun FastAPI server
inv db.drop -e [env]  # drop all db tables
inv db.migrate -e [env]  # run db schema migrations
inv db.reset -e [env]  # reset all database tables (drop + migrate)
inv db.wipe -e [env]  # delete dev or test sqlite file
inv db.revision  # generate migration script with Alembic (autogeneration with the latest SQLAlchemy models)
inv quality.style  # examine coding style with flake8
inv quality.metric  # measure code metric with radon
inv quality.all  # run all quality tasks (style + metric)
inv quality.reformat  # reformat your code using the black code style
inv quality  # same as `inv quality.all`
inv rmvcr  # delete cassette fixtures (test stubs generated with vcrpy)
```
