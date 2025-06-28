import pathlib

from mtgjson.mtgjson5.output_generator import write_set_file
from mtgjson.mtgjson5.output_generator import generate_compiled_prices_output
from mtgjson.mtgjson5.output_generator import build_format_specific_files
from mtgjson.mtgjson5.output_generator import build_atomic_specific_files
from mtgjson.mtgjson5.output_generator import build_price_specific_files
from mtgjson.mtgjson5.output_generator import build_all_printings_files
from mtgjson.mtgjson5.output_generator import generate_compiled_output_files
from mtgjson.mtgjson5.output_generator import create_compiled_output
from mtgjson.mtgjson5.output_generator import write_compiled_output_to_file
from mtgjson.mtgjson5.output_generator import construct_format_map
from mtgjson.mtgjson5.output_generator import construct_atomic_cards_format_map
from mtgjson.mtgjson5.output_generator import generate_output_file_hashes

from mtgjson.mtgjson5.classes import MtgjsonSetObject
from mtgjson.mtgjson5.compiled_classes import MtgjsonAllPrintingsObject


def test_PT_write_set_file():
    so = MtgjsonSetObject() 
    write_set_file(so, True)

def test_PT_generate_compiled_prices_output():
    pd = {"test": {"test1": 1.23}}
    generate_compiled_prices_output(pd, False)

def test_PT_build_format_specific_files():
    ap = MtgjsonAllPrintingsObject()
    build_format_specific_files(ap, False)

def test_PT_build_atomic_specific_files():
    build_atomic_specific_files(True)

def test_PT_build_price_specific_files():
    build_price_specific_files(False)

def test_PT_build_all_printings_files():
    build_all_printings_files(True)

def test_PT_generate_compiled_output_files():
    generate_compiled_output_files(False)

def test_PT_create_compiled_output():
    create_compiled_output("testname", compiled_object, True)

def test_PT_write_compiled_output_to_file():
    write_compiled_output_to_file("testname",file_contents,True)

def test_PT_construct_format_map():
    p = pathlib.Path('/testpath')
    construct_format_map(p)

def test_PT_construct_atomic_cards_format_map():
    p = pathlib.Path('/testpath')
    construct_atomic_cards_format_map(p)

def test_PT_generate_output_file_hashes():
    p = pathlib.Path('/testpath')
    generate_output_file_hashes(p)
