from invoke import task


@task(
    help={
        "code": "Name of the python script or pacakge to measure the test coverage. Default: '.'"
    }
)
def spec(c, code="."):
    """
    run tests
    """
    c.run(f"pytest --cov={code} -s -v spec/*_spec.py", pty=True)
