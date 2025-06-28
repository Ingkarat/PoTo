"""
This file contains all violations which may be tweaked using
`i_control_code` or `i_dont_control_code` options.

It is used for some of e2e tests to check that `i_control_code` works.
"""
import sys as sys

def __getattr__():
    anti_z428 = 1