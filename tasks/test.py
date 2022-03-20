from invoke import task


@task(
    default=True,
    help={
        "code": "Name of the python script or pacakge to measure the test coverage. Default: '.'"
    },
)
def test(c, code="."):
    """
    Run tests (need to run `inv worker.run.test` in another process)
    """
    c.run(
        f"pytest -s -v --cov={code} --cov-report=xml:./coverage/reports/coverage.xml --cov-config=.coveragerc",
        pty=True,
    )
