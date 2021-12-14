from invoke import task

from config import get_settings


@task(
    default=True,
    help={
        "mode": "Deployment mode for running API server. ['test'|'development'|'production'] [default: 'development']",
        "reload": "Restart your app when a file changes. This consumes much more resources and is more unstable. It helps a lot during development, but you shouldn't use it in production. [default: False]",
        "port": "Bind socket to this port.  [default: 8000]",
    },
)
def run(c, mode="development", reload=False, port=8000):
    """
    Run fastapi server with specified settings
    """
    if reload:
        c.run(
            f"ENV={mode} uvicorn application.app:app --reload --reload-exclude {get_settings().REPOSTORE_PATH} --port {port}",
            pty=True,
        )
    else:
        c.run(f"ENV={mode} uvicorn application.app:app --port {port}", pty=True)


@task(help={"port": "Bind socket to this port.  [default: 8000]"})
def dev(c, port=8000):
    """
    Rerun fastapi server in development environment
    """
    print("REMEMBER: need to run `inv worker.run.dev` in another process")
    c.run(
        f"ENV=development uvicorn application.app:app --reload --reload-exclude {get_settings().REPOSTORE_PATH} --port {port}",
        pty=True,
    )


@task(help={"port": "Bind socket to this port.  [default: 8080]"})
def test(c, port=8080):
    """
    Run fastapi server in test environment
    """
    print("REMEMBER: need to run `inv worker.run.test` in another process")
    c.run(f"ENV=test uvicorn application.app:app --port {port}", pty=True)
