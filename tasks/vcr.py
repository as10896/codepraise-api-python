from invoke import task


@task
def delete(c):
    """
    Delete cassette fixtures
    """
    result = c.run("rm tests/fixtures/cassettes/*.yml", hide=True, warn=True)
    if result.ok:
        print("Cassettes deleted")
    else:
        print("No cassettes found")
