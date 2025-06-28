import os
import subprocess
import pytest

def TestBokehJS_test_bokehjs(self) -> None:
    os.chdir('bokehjs')
    proc = subprocess.Popen(['node', 'make', 'test'], stdout=subprocess.PIPE)
    (out, errs) = proc.communicate()
    msg = out.decode('utf-8', errors='ignore')
    os.chdir('..')
    print(msg)
    if proc.returncode != 0:
        assert False