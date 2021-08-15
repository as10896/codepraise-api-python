from invoke import task


@task(
    help={
        "mode": "Deployment mode for running API server. ['test'|'development'|'production'] [default: 'development']",
        "port": "Bind socket to this port.  [default: 8000]",
    }
)
def run(c, mode="development", port=8000):
    """
    rerun fastapi server
    """
    c.run(f"ENV={mode} uvicorn app:app --reload --port {port}", pty=True)
