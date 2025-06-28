from invoke.util import helpline

def helpline_is_None_if_no_docstring(self):

    def foo(c):
        pass
    assert helpline(foo) is None

def helpline_is_entire_thing_if_docstring_one_liner(self):

    def foo(c):
        """foo!"""
        pass
    assert helpline(foo) == 'foo!'

def helpline_left_strips_newline_bearing_one_liners(self):

    def foo(c):
        """
                foo!
                """
        pass
    assert helpline(foo) == 'foo!'

def helpline_is_first_line_in_multiline_docstrings(self):

    def foo(c):
        """
                foo?

                foo!
                """
        pass
    assert helpline(foo) == 'foo?'

def helpline_is_None_if_docstring_matches_object_type(self):

    class Foo(object):
        """I am Foo"""
        pass
    foo = Foo()
    assert helpline(foo) is None

def helpline_instance_attached_docstring_is_still_displayed(self):

    class Foo(object):
        """I am Foo"""
        pass
    foo = Foo()
    foo.__doc__ = 'I am foo'
    assert helpline(foo) == 'I am foo'