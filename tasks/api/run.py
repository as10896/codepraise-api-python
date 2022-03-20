from invoke import task

from config import get_settings


@task(
    default=True,
    help={
        "env": "Deployment environment for running API server. ['test'|'development'|'production'] [default: 'development']",
        "reload": "Restart your app when a file changes. This consumes much more resources and is more unstable. It helps a lot during development, but you shouldn't use it in production. [default: False]",
        "port": "Bind socket to this port. [default: 8000]",
        "host": "Bind socket to this host. [default: 127.0.0.1]",
    },
)
def run(c, env="development", reload=False, port=8000, host="127.0.0.1"):
    """
    Run fastapi server with specified settings
    """
    cmd = f"ENV={env} uvicorn app.application.app:app"

    if reload:
        cmd = f"{cmd} --reload --reload-exclude {get_settings().REPOSTORE_PATH}"

    c.run(f"{cmd} --host {host} --port {port}", pty=True)


@task(
    help={
        "port": "Bind socket to this port. [default: 8000]",
        "host": "Bind socket to this host. [default: 127.0.0.1]",
    }
)
def dev(c, port=8000, host="127.0.0.1"):
    """
    Rerun fastapi server in development environment
    """
    print("REMEMBER: need to run `inv worker.run.dev` in another process")
    c.run(
        f"ENV=development uvicorn app.application.app:app --reload --reload-exclude {get_settings().REPOSTORE_PATH} --host {host} --port {port}",
        pty=True,
    )


@task(
    help={
        "port": "Bind socket to this port. [default: 8080]",
        "host": "Bind socket to this host. [default: 127.0.0.1]",
    }
)
def test(c, port=8080, host="127.0.0.1"):
    """
    Run fastapi server in test environment
    """
    print("REMEMBER: need to run `inv worker.run.test` in another process")
    c.run(
        f"ENV=test uvicorn app.application.app:app --host {host} --port {port}",
        pty=True,
    )


@task(
    help={
        "port": "Bind socket to this port. [default: 8000]",
        "host": "Bind socket to this host. [default: 0.0.0.0]",
        "workers": "The number of worker processes for handling requests. [default: 4]",
    }
)
def prod(c, port=8000, host="0.0.0.0", workers=4):
    """
    Run fastapi server in production environment
    """
    print("REMEMBER: need to run `inv worker.run.prod` in another process")
    c.run(
        f"gunicorn app.application.app:app --workers {workers} --worker-class uvicorn.workers.UvicornWorker --env ENV=production --bind {host}:{port}",
        pty=True,
    )
