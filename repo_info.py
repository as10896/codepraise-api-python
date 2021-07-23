import requests
import yaml


with open("config/secrets.yml") as f:
    config = yaml.safe_load(f)


def gh_api_path(path):
    return f"https://api.github.com/repos/{path}"


def call_gh_url(config, url):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {config['gh_token']}"
    }
    res = requests.get(url, headers=headers)
    return res


gh_response = {}
gh_results = {}

## GOOD REPO (HAPPY)
repo_url = gh_api_path("allenai/science-parse")
gh_response["repo"] = call_gh_url(config, repo_url)
repo = gh_response["repo"].json()

gh_results["size"] = repo["size"]
# should be 77098

gh_results["owner"] = repo["owner"]
# should have info about allenai

gh_results["git_url"] = repo["git_url"]
# should be "git://github.com/allenai/science-parse.git"

gh_results["contributors_url"] = repo["contributors_url"]
# should be "https://api.github.com/repos/allenai/science-parse/contributors"

contributors_url = repo['contributors_url']
gh_response["contributors"] = call_gh_url(config, contributors_url)
contributors = gh_response["contributors"].json()

gh_results["contributors"] = contributors
len(contributors)
# should be 12 contributors array

contributors = list(map(lambda c: c["login"], contributors))
# should be ['dirkgr', 'dcdowney', 'amosjyng', 'aria42', 'rreas', 'rjpower', 'jpowerwa', 'chrisc36', 'rodneykinney', 'bbstilson', 'dirkraft', 'nalourie-ai2']


## BAD REPO (SAD)
bad_repo_url = gh_api_path('allenai/foobar')
gh_response[bad_repo_url] = call_gh_url(config, bad_repo_url)
gh_response[bad_repo_url].json()   # makes sure any streaming finishes


with open("spec/fixtures/gh_response.yml", "w") as f:
    yaml.dump(gh_response, f, allow_unicode=True)

with open("spec/fixtures/gh_results.yml", "w") as f:
    yaml.dump(gh_results, f, allow_unicode=True)
