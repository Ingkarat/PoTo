from invoke import task, Collection
from . import build, deploy, provision

@task(aliases=['ipython'])
def shell(c):
    """Load a REPL with project state already set up."""
    pass

@task(aliases=['run_tests'], default=True)
def test(c):
    """Run the test suite with baked-in args."""
    pass
localbuild = build.ns
localbuild.__doc__ = build.__doc__
ns = Collection(shell, test, deploy, provision, build=localbuild)