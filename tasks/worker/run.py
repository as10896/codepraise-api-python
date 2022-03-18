from invoke import task


@task(
    help={
        "processes": "Number of child processes processing the queue. If 0 is specified, the number of CPUs available on your system will be used. [default: 1]"
    }
)
def dev(c, processes=1):
    """
    Run the background celery worker in development mode
    """
    cmd = "ENV=development celery --app=workers.clone_repo_worker:celery worker --loglevel=INFO"

    if processes:
        cmd = f"{cmd} --concurrency={processes}"

    c.run(cmd, pty=True)


@task(
    help={
        "processes": "Number of child processes processing the queue. If 0 is specified, the number of CPUs available on your system will be used. [default: 1]"
    }
)
def test(c, processes=1):
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
        "processes": "Number of child processes processing the queue. If 0 is specified, the number of CPUs available on your system will be used. [default: 0]"
    }
)
def prod(c, processes=0):
    """
    Run the background celery worker in production mode
    """
    cmd = "ENV=production celery --app=workers.clone_repo_worker:celery worker --loglevel=INFO"
    if processes:
        cmd = f"{cmd} --concurrency={processes}"
    c.run(cmd, pty=True)
