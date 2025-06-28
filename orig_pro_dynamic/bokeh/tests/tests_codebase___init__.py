from os.path import abspath, join, pardir, split
from subprocess import run
from typing import List
TOP_PATH = abspath(join(split(__file__)[0], pardir, pardir))

def ls_files(*patterns: str) -> List[str]:
    proc = run(['git', 'ls-files', '--', *patterns], capture_output=True)
    return proc.stdout.decode('utf-8').split('\n')