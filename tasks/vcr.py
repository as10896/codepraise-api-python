from invoke import task


@task
def delete(c):
    """
    Delete cassette fixtures
    """
    result = c.run("rm spec/fixtures/cassettes/*.yml", hide=True, warn=True)
    if result.ok:
        print("Cassettes deleted")
    else:
        print("No cassettes found")
