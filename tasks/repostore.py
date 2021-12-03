from invoke import task
from config import get_settings


@task
def list(c):
    """
    List cloned repos in repo store
    """
    c.run(f"ls {get_settings().REPOSTORE_PATH}", pty=True)
