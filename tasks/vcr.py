from invoke import task


@task
def rmvcr(c):
    """
    delete cassette fixtures
    """
    result = c.run("rm spec/fixtures/cassettes/*.yml", hide=True, warn=True)
    if result.ok:
        print("Cassettes deleted")
    else:
        print("No cassettes found")
