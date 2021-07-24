from invoke import task, UnexpectedExit


@task
def wipe(c):
    """
    delete cassette fixtures
    """
    try:
        c.run("rm spec/fixtures/cassettes/*.yml")
        print("Cassettes deleted")
    except UnexpectedExit:
        print("No cassettes found")
