from invoke import task

@task
def go(c):
    return c

@task
def check_warn(c):
    assert c.config.run.warn is True

@task
def check_pty(c):
    assert c.config.run.pty is True

@task
def check_hide(c):
    assert c.config.run.hide == 'both'

@task
def check_echo(c):
    assert c.config.run.echo is True