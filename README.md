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

# Usage

### Test Github API
Save the HTTP resopnse and the parsed data into yaml files
```bash
python repo_info.py
```
It'll generate following files under `spec/fixtures`

* `gh_response.yml` - the original HTTP resopnse <br>
    Note that this file contains your request header, which includes your personal token.<br>
    **DO NOT** put this file to the public.
* `gh_results.yml` - parsed results from HTTP response

### Testing
```bash
pytest -v spec/repo_spec.py  # run testing script
```

This should fail one test (we use cache, so there's no opportunity to raise exception).
