from invoke import task


@task(help={"code": "Name of the python script or pacakge to measure code metric. Default: 'lib/'"})
def metric(c, code="lib/"):
    """
    measure code metric with radon
    """
    print("Code metrics:\n")
    c.run(f"radon cc {code}", pty=True)
    print("\n")


@task(help={"code": "Name of the python script or pacakge to examine coding style. Default: '.'"})
def style(c, code="."):
    """
    examine coding style with flake8
    """
    print("Coding style check:\n")
    c.run(f"flake8 {code} --exit-zero", pty=True)
    print("\n")


@task(post=[style, metric], default=True)
def all(c):
    """
    run all quality tasks (style + metric)
    """
    print("Run all quality tests...\n")


@task(help={"code": "Name of the python script or pacakge to reformat. Default: '.'"})
def reformat(c, code="."):
    """
    reformat your code using the black code style
    """
    c.run(f"black {code}", pty=True)
