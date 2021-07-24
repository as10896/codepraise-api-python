from invoke import task


@task
def radon(c, CODE="lib/"):
    """
    measure code metric
    """
    print("Code metrics:\n")
    c.run(f"radon cc {CODE}", pty=True)
    print("\n")


@task
def flake8(c):
    """
    examine coding style
    """
    print("Coding style check:\n")
    c.run("flake8 .", pty=True)
    print("\n")


@task(post=[radon, flake8], default=True)
def all(c):
    """
    run all quality test
    """
    print("Run all quality tests...\n")
