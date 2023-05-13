from invoke import task


@task
def start(ctx):
    ctx.run("python3 src/index.py", pty=True)


@task
def test(ctx):
    ctx.run("pytest src", pty=True)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)


@task
def format(ctx):
    # backend_test.py sets an envvar, autopep8 "fixed" the import order,
    # hence testing reverted to PROD database instead of ":memory:" DEV
    ctx.run("autopep8 --in-place --recursive --exclude *_test.py src", pty=True)


@task
def lint(ctx):
    ctx.run("pylint src", pty=True)
