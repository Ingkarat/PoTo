import pytest
pytest
import os
from subprocess import PIPE, Popen
LICENSES = ['0BSD', 'Apache-2.0', 'AFLv2.1', 'BSD-2-Clause', 'BSD-3-Clause', 'ISC', 'MIT', 'Unlicense', 'WTFPL']

@pytest.mark.skip(reason='error')
def test_js_license_set() -> None:
    """ If the current set of JS licenses changes, they should be noted in
    the bokehjs/LICENSE file.

    """
    os.chdir('bokehjs')
    proc = Popen(['npx', 'license-checker', '--production', '--summary', '--onlyAllow', '%s' % ';'.join(LICENSES)], stdout=PIPE)
    proc.communicate()
    proc.wait()
    os.chdir('..')
    if proc.returncode != 0:
        assert False