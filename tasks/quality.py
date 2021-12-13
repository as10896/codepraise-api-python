from invoke import task


@task(
    help={
        "code": "Name of the python script or pacakge to measure code metric. Default: '.'"
    }
)
def metric(c, code="."):
    """
    Measure code metric with radon
    """
    print("Code metrics:\n")
    c.run(f"radon cc {code}", pty=True)
    print("\n")


@task(
    help={
        "code": "Name of the python script or pacakge to examine coding style. Default: '.'"
    }
)
def style(c, code="."):
    """
    Examine coding style with flake8
    """
    print("Coding style check:\n")
    c.run(f"flake8 {code} --exit-zero", pty=True)
    print("\n")


@task(
    default=True,
    help={
        "code": "Name of the python script or pacakge to run quality tasks. Default: '.'"
    },
)
def all(c, code="."):
    """
    Run all quality tasks (style + metric)
    """
    print("Run all quality tests...\n")
    style(c, code)
    metric(c, code)


@task(help={"code": "Name of the python script or pacakge to reformat. Default: '.'"})
def reformat(c, code="."):
    """
    Reformat your code using the black coding style
    """
    c.run(f"black {code}", pty=True)


@task(
    help={
        "code": "Name of the python script or package to check type with mypy. Default: '.'"
    }
)
def typecheck(c, code="."):
    """
    Type checking with mypy
    """
    c.run(f"mypy {code} --config-file mypy.ini", pty=True)
