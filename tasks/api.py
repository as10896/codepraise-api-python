from invoke import task


@task(
    help={
        "mode": "Deployment mode for running API server. ['test'|'development'|'production'] [default: 'test']"
    }
)
def run(c, mode="test"):
    """
    rerun fastapi server
    """
    c.run(f"ENV={mode} uvicorn main:app --reload", pty=True)
