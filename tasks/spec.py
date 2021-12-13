from invoke import task


@task(
    default=True,
    help={
        "code": "Name of the python script or pacakge to measure the test coverage. Default: '.'"
    },
)
def spec(c, code="."):
    """
    Run tests (need to run `inv worker.run.test` in another process)
    """
    c.run(
        f"pytest -s -v spec/*_spec.py --cov={code} --cov-report=xml --cov-config=.coveragerc",
        pty=True,
    )
