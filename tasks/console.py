from invoke import task


@task(
    default=True,
    help={
        "env": "Environment of the console to run. ['test'|'development'|'production'] [default: 'development']"
    },
)
def console(c, env="development"):
    """
    Run application console (ipython)
    """
    c.run(f"ENV={env} ipython -i tests/load_all.py", pty=True)
