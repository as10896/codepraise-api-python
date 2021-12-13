from invoke import task


@task(
    help={
        "processes": "Number of child processes processing the queue. If not specified, the number of CPUs available on your system will be used."
    }
)
def dev(c, processes=None):
    """
    Run the background celery worker in development mode
    """
    cmd = "ENV=development celery --app=workers.clone_repo_worker:celery worker --loglevel=INFO"

    if processes:
        cmd = f"{cmd} --concurrency={processes}"

    c.run(cmd, pty=True)


@task(
    help={
        "processes": "Number of child processes processing the queue. If not specified, the number of CPUs available on your system will be used."
    }
)
def test(c, processes=None):
    """
    Run the background celery worker in test mode
    """
    cmd = (
        "ENV=test celery --app=workers.clone_repo_worker:celery worker --loglevel=INFO"
    )
    if processes:
        cmd = f"{cmd} --concurrency={processes}"
    c.run(cmd, pty=True)


@task(
    help={
        "processes": "Number of child processes processing the queue. If not specified, the number of CPUs available on your system will be used."
    }
)
def prod(c, processes=None):
    """
    Run the background celery worker in production mode
    """
    cmd = "ENV=production celery --app=workers.clone_repo_worker:celery worker --loglevel=INFO"
    if processes:
        cmd = f"{cmd} --concurrency={processes}"
    c.run(cmd, pty=True)
