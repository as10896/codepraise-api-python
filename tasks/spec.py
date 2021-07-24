from invoke import task


@task
def spec(c, CODE="lib/"):
    """
    run tests
    """
    c.run(f"pytest --cov={CODE} -v spec/repo_spec.py", pty=True)
