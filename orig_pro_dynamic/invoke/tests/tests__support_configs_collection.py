from invoke import ctask, Collection

@ctask
def go(c):
    c.run('false')
ns = Collection(go)
ns.configure({'run': {'echo': True}})