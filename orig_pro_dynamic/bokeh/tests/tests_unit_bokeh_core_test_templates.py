import pytest
pytest
import hashlib
from os.path import abspath, join, split
import bokeh.core.templates as bct
TOP_PATH = abspath(join(split(bct.__file__)[0]))

def _crlf_cr_2_lf_bin(s):
    import re
    return re.sub(b'\r\n|\r|\n', b'\n', s)

def compute_sha256(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()
pinned_template_sha256 = 'f3667e80d84d19b7d2b0642a3dd17131b72c0468981a3dd08227345d1fb2cfe5'

def test_autoload_template_has_changed() -> None:
    """This is not really a test but a reminder that if you change the
    autoload_nb_js.js template then you should make sure that insertion of
    plots into notebooks is working as expected. In particular, this test was
    created as part of https://github.com/bokeh/bokeh/issues/7125.
    """
    with open(join(TOP_PATH, '_templates/autoload_nb_js.js'), mode='rb') as f:
        current_template_sha256 = compute_sha256(_crlf_cr_2_lf_bin(f.read()))
        assert pinned_template_sha256 == current_template_sha256, '            It seems that the template autoload_nb_js.js has changed.\n            If this is voluntary and that proper testing of plots insertion\n            in notebooks has been completed successfully, update this test\n            with the new file SHA256 signature.'