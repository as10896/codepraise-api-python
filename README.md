# codepraise-api-python

## Prerequisite
### Create virtual environment
Here we use `pipenv` to create our virtual environment.

```bash
pip install pipenv  # install pipenv
pipenv --three  # create Python 3 virtualenv under current directory (will create a `Pipfile` as well)
pipenv shell  # activate the virtualenv of the current directory
pipenv install  # install required dependencies with Pipfile (or Pipfile.lock, if any)
```

### Create GitHub API personal access token
1. Generate token [here](https://github.com/settings/tokens)
2. Create `config/secrets.yml` with the generated token
```yaml
---
gh_token: '<your_personal_token>'
```

## Usage
Here we use [invoke](https://docs.pyinvoke.org/) as our task management tool

```bash
inv -l  # show all tasks
inv spec  # run test script
inv quality.flake8  # examine code style
inv quality.radon  # measure code metric
inv quality.all  # run all code quality checking tasks
inv quality  # same as `inv quality.all`
inv vcr.wipe  # delete cassette fixtures (test stubs generated with vcrpy)
```
