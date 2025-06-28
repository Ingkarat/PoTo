import os
import sys
from invoke import Program
import pytest
from _util import expect, trap, ROOT
pytestmark = pytest.mark.usefixtures('integration')

@trap
def _complete(invocation, collection=None, **kwargs):
    colstr = ''
    if collection:
        colstr = '-c {}'.format(collection)
    command = 'inv --complete {0} -- inv {0} {1}'.format(colstr, invocation)
    Program(**kwargs).run(command, exit=False)
    return sys.stdout.getvalue()

def _assert_contains(haystack, needle):
    assert needle in haystack

def CompletionScriptPrinter_setup(self):
    self.prev_cwd = os.getcwd()
    os.chdir(ROOT)

def CompletionScriptPrinter_teardown(self):
    os.chdir(self.prev_cwd)

def CompletionScriptPrinter_only_accepts_certain_shells(self):
    expect('--print-completion-script', err='needed value and was not given one', test=_assert_contains)
    expect('--print-completion-script bla', err='Completion for shell "bla" not supported (options are: bash, fish, zsh).', test=_assert_contains)

def CompletionScriptPrinter_prints_for_custom_binary_names(self):
    (out, err) = expect('myapp --print-completion-script zsh', program=Program(binary_names=['mya', 'myapp']), invoke=False)
    assert '_complete_mya() {' in out
    assert 'invoke' not in out
    assert ' mya myapp' in out

def CompletionScriptPrinter_default_binary_names_is_completing_argv_0(self):
    (out, err) = expect('someappname --print-completion-script zsh', program=Program(binary_names=None), invoke=False)
    assert '_complete_someappname() {' in out
    assert ' someappname' in out

def CompletionScriptPrinter_bash_works(self):
    (out, err) = expect('someappname --print-completion-script bash', invoke=False)
    assert '_complete_someappname() {' in out
    assert 'complete -F' in out
    for line in out.splitlines():
        if line.startswith('complete -F'):
            assert line.endswith(' someappname')

def CompletionScriptPrinter_fish_works(self):
    (out, err) = expect('someappname --print-completion-script fish', invoke=False)
    assert 'function __complete_someappname' in out
    assert 'complete --command someappname' in out

def ShellCompletion_no_input_means_just_task_names(self):
    expect('-c simple_ns_list --complete', out='z-toplevel\na.b.subtask\n')

def ShellCompletion_custom_binary_name_completes(self):
    expect('myapp -c integration --complete -- ba', program=Program(binary='myapp'), invoke=False, out='bar', test=_assert_contains)

def ShellCompletion_aliased_custom_binary_name_completes(self):
    for used_binary in ('my', 'myapp'):
        expect('{0} -c integration --complete -- ba'.format(used_binary), program=Program(binary='my[app]'), invoke=False, out='bar', test=_assert_contains)

def ShellCompletion_no_input_with_no_tasks_yields_empty_response(self):
    expect('-c empty --complete', out='')

def ShellCompletion_task_name_completion_includes_aliases(self):
    for name in ('z\n', 'toplevel'):
        assert name in _complete('', 'alias_sorting')

def ShellCompletion_top_level_with_dash_means_core_options(self):
    output = _complete('-')
    for flag in ('--no-dedupe', '-d', '--debug', '-V', '--version'):
        assert '{}\n'.format(flag) in output

def ShellCompletion_bare_double_dash_shows_only_long_core_options(self):
    output = _complete('--')
    assert '--no-dedupe' in output
    assert '-V' not in output

def ShellCompletion_task_names_only_complete_other_task_names(self):
    assert 'print-name' in _complete('print-foo', 'integration')

def ShellCompletion_task_name_completion_includes_tasks_already_seen(self):
    assert 'print-foo' in _complete('print-foo', 'integration')

def ShellCompletion_per_task_flags_complete_with_single_dashes(self):
    for flag in ('--name', '-n'):
        assert flag in _complete('print-name -', 'integration')

def ShellCompletion_per_task_flags_complete_with_double_dashes(self):
    output = _complete('print-name --', 'integration')
    assert '--name' in output
    assert '-n\n' not in output

def ShellCompletion_flag_completion_includes_inverse_booleans(self):
    output = _complete('basic-bool -', 'foo')
    assert '--no-mybool' in output

def ShellCompletion_tasks_with_positional_args_complete_with_flags(self):
    output = _complete('print-name --', 'integration')
    assert '--name' in output

def ShellCompletion_core_flags_taking_values_have_no_completion_output(self):
    assert _complete('-f') == ''

def ShellCompletion_per_task_flags_taking_values_have_no_completion_output(self):
    assert _complete('basic-arg --arg', 'foo') == ''

def ShellCompletion_core_bool_flags_have_task_name_completion(self):
    assert 'mytask' in _complete('--echo', 'foo')

def ShellCompletion_per_task_bool_flags_have_task_name_completion(self):
    assert 'mytask' in _complete('basic-bool --mybool', 'foo')

def ShellCompletion_core_partial_or_invalid_flags_print_all_flags(self):
    for flag in ('--echo', '--complete'):
        for given in ('--e', '--nope'):
            assert flag in _complete(given)

def ShellCompletion_per_task_partial_or_invalid_flags_print_all_flags(self):
    for flag in ('--arg1', '--otherarg'):
        for given in ('--ar', '--nope'):
            completion = _complete('multiple-args {}'.format(given), 'foo')
            assert flag in completion