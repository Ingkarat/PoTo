import pathlib

from mtgjson.mtgjson5.utils import init_logger
from mtgjson.mtgjson5.utils import url_keygen
from mtgjson.mtgjson5.utils import to_camel_case
from mtgjson.mtgjson5.utils import parse_magic_rules_subset
from mtgjson.mtgjson5.utils import retryable_session
from mtgjson.mtgjson5.utils import parallel_call
from mtgjson.mtgjson5.utils import sort_internal_lists
from mtgjson.mtgjson5.utils import fix_windows_set_name
from mtgjson.mtgjson5.utils import get_file_hash
from mtgjson.mtgjson5.utils import get_str_or_none
from mtgjson.mtgjson5.utils import send_push_notification
from mtgjson.mtgjson5.utils import deep_merge_dictionaries
from mtgjson.mtgjson5.utils import get_all_cards_and_tokens_from_content
from mtgjson.mtgjson5.utils import get_all_cards_and_tokens
from mtgjson.mtgjson5.utils import generate_card_mapping


def test_PT_init_logger():
    init_logger()

def test_PT_url_keygen():
    url_keygen(1, True)
    url_keygen("a", False)

def test_PT_to_camel_case():
    to_camel_case("teststr")

def test_PT_parse_magic_rules_subset():
    parse_magic_rules_subset("teststr","teststr","teststr")

def test_PT_retryable_session():
    retryable_session(8)

def test_PT_parallel_call():
    parallel_call(f,a,(1,2))
    parallel_call(f,a,[1,2])

def test_PT_sort_internal_lists():
    sort_internal_lists(data)

def test_PT_fix_windows_set_name():
    fix_windows_set_name("name")

def test_PT_get_file_hash():
    p = pathlib.Path('/testpath')
    get_file_hash(p, 1)

def test_PT_get_str_or_none():
    get_str_or_none(v)

def test_PT_send_push_notification():
    send_push_notification("teststr")

def test_PT_deep_merge_dictionaries():
    deep_merge_dictionaries({"a",1})

def test_PT_get_all_cards_and_tokens_from_content():
    get_all_cards_and_tokens_from_content({"a",1})

def test_PT_get_all_cards_and_tokens():
    p = pathlib.Path('/testpath')
    get_all_cards_and_tokens(p)
    
def test_PT_generate_card_mapping():
    p = pathlib.Path('/testpath')
    l = ("a","b")
    r = ("x","y")
    generate_card_mapping(p,l,r)
