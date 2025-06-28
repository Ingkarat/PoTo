import pathlib

from mtgjson.mtgjson5.compress_generator import compress_mtgjson_contents

def test_PT_compress_mtgjson_contents():
    p = pathlib.Path('/testpath')
    compress_mtgjson_contents(p)