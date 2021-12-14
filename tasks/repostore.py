from invoke import task

from config import get_settings


@task
def create(c):
    """
    Create the directory of repostore path
    """
    c.run(f"mkdir {get_settings().REPOSTORE_PATH}", pty=True)


@task
def delete(c):
    """
    Delete cloned repos in repo store
    """
    result = c.run(f"rm -rf {get_settings().REPOSTORE_PATH}/*", hide=True, warn=True)
    if result.ok:
        print("Cloned repos deleted")
    else:
        print("Could not delete cloned repos")


@task
def list(c):
    """
    List cloned repos in repo store
    """
    c.run(f"ls {get_settings().REPOSTORE_PATH}", pty=True)
