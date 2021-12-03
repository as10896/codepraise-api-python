from invoke import task


@task(
    help={
        "mode": "Environment of the console mode to run. ['test'|'development'|'production'] [default: 'test']"
    }
)
def console(c, mode="test"):
    """
    run application console (ipython)
    """
    c.run(f"ENV={mode} ipython -i spec/test_load_all.py", pty=True)
