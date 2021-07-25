from invoke import task


@task(help={"code": "Name of the python script or pacakge to measure the test coverage. Default: 'lib/'"})
def spec(c, code="lib/"):
    """
    run tests
    """
    c.run(f"pytest --cov={code} -v spec/repo_spec.py", pty=True)
