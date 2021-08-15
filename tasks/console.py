from invoke import task


@task
def console(c, mode="test"):
    """
    run console
    """
    c.run(f"ENV={mode} ipython -i spec/test_load_all.py", pty=True)
