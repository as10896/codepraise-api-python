# codepraise-api-python
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Prerequisite
### Create virtual environment
Here we use [Pipenv](https://pipenv.pypa.io/en/latest/) to create our virtual environment.

```bash
pip install pipenv  # install pipenv
pipenv --three  # create Python 3 virtualenv under current directory
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
inv [task] -h  # show task help message
inv spec  # run test script
inv quality.style  # examine coding style with flake8
inv quality.metric  # measure code metric with radon
inv quality.all  # run all quality tasks (style + metric)
inv quality.reformat  # reformat your code using the black code style
inv quality  # same as `inv quality.all`
inv vcr.wipe  # delete cassette fixtures (test stubs generated with vcrpy)
```
