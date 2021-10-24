from invoke import task


@task(
    default=True,
    help={
        "code": "Name of the python script or pacakge to measure the test coverage. Default: '.'"
    },
)
def spec(c, code="."):
    """
    run tests
    """
    c.run(f"pytest -s -v spec/*_spec.py --cov={code} --cov-report=xml --cov-config=.coveragerc", pty=True)


@task(
    help={
        "code": "Name of the python script or package to check type with mypy. Default: '.'"
    }
)
def type(c, code="."):
    """
    type checking with mypy
    """
    c.run(f"mypy {code} --config-file mypy.ini", pty=True)
