import json
import os
import sys
from invoke.util import six, Lexicon
from mock import patch, Mock, ANY
import pytest
from pytest import skip
from pytest_relaxed import trap
from invoke import Argument, Collection, Config, Executor, FilesystemLoader, ParserContext, ParseResult, Program, Result, Task, UnexpectedExit
from invoke import main
from invoke.util import cd
from invoke.config import merge_dicts
from _util import ROOT, expect, load, run, skip_if_windows, support_file, support_path
pytestmark = pytest.mark.usefixtures('integration')

def init_may_specify_version(self):
    assert Program(version='1.2.3').version == '1.2.3'

def init_default_version_is_unknown(self):
    assert Program().version == 'unknown'

def init_may_specify_namespace(self):
    foo = load('foo')
    assert Program(namespace=foo).namespace is foo

def init_may_specify_name(self):
    assert Program(name='Myapp').name == 'Myapp'

def init_may_specify_binary(self):
    assert Program(binary='myapp').binary == 'myapp'

def init_loader_class_defaults_to_FilesystemLoader(self):
    assert Program().loader_class is FilesystemLoader

def init_may_specify_loader_class(self):
    klass = object()
    assert Program(loader_class=klass).loader_class == klass

def init_executor_class_defaults_to_Executor(self):
    assert Program().executor_class is Executor

def init_may_specify_executor_class(self):
    klass = object()
    assert Program(executor_class=klass).executor_class == klass

def init_config_class_defaults_to_Config(self):
    assert Program().config_class is Config

def init_may_specify_config_class(self):
    klass = object()
    assert Program(config_class=klass).config_class == klass

def miscellaneous_debug_flag_activates_logging(self):
    with patch('invoke.util.debug') as debug:
        Program().run('invoke -d -c debugging foo')
        debug.assert_called_with('my-sentinel')

def miscellaneous_debug_honored_as_env_var_too(self, reset_environ):
    os.environ['INVOKE_DEBUG'] = '1'
    with patch('invoke.util.debug') as debug:
        Program().run('invoke -c debugging foo')
        debug.assert_called_with('my-sentinel')

def miscellaneous_bytecode_skipped_by_default(self):
    expect('-c foo mytask')
    assert sys.dont_write_bytecode

def miscellaneous_write_pyc_explicitly_enables_bytecode_writing(self):
    expect('--write-pyc -c foo mytask')
    assert not sys.dont_write_bytecode

@patch('invoke.program.sys')
def normalize_argv_defaults_to_sys_argv(self, mock_sys):
    argv = ['inv', '--version']
    mock_sys.argv = argv
    p = Program()
    p.print_version = Mock()
    p.run(exit=False)
    p.print_version.assert_called()

def normalize_argv_uses_a_list_unaltered(self):
    p = Program()
    p.print_version = Mock()
    p.run(['inv', '--version'], exit=False)
    p.print_version.assert_called()

def normalize_argv_splits_a_string(self):
    p = Program()
    p.print_version = Mock()
    p.run('inv --version', exit=False)
    p.print_version.assert_called()

def name_defaults_to_capitalized_binary_when_None(self):
    expect('myapp --version', out='Myapp unknown\n', invoke=False)

def name_benefits_from_binary_absolute_behavior(self):
    """benefits from binary()'s absolute path behavior"""
    expect('/usr/local/bin/myapp --version', out='Myapp unknown\n', invoke=False)

def name_uses_overridden_value_when_given(self):
    p = Program(name='NotInvoke')
    expect('--version', out='NotInvoke unknown\n', program=p)

def binary_defaults_to_argv_when_None(self):
    (stdout, _) = run('myapp --help', invoke=False)
    assert 'myapp [--core-opts]' in stdout

def binary_uses_overridden_value_when_given(self):
    (stdout, _) = run('myapp --help', invoke=False, program=Program(binary='nope'))
    assert 'nope [--core-opts]' in stdout

@trap
def binary_use_binary_basename_when_invoked_absolutely(self):
    Program().run('/usr/local/bin/myapp --help', exit=False)
    stdout = sys.stdout.getvalue()
    assert 'myapp [--core-opts]' in stdout
    assert '/usr/local/bin' not in stdout

@trap
def called_as_is_the_whole_deal_when_just_a_name(self):
    p = Program()
    p.run('whatever --help', exit=False)
    assert p.called_as == 'whatever'

@trap
def called_as_is_basename_when_given_a_path(self):
    p = Program()
    p.run('/usr/local/bin/whatever --help', exit=False)
    assert p.called_as == 'whatever'

def binary_names_defaults_to_argv_when_None(self):
    (stdout, _) = run('foo --print-completion-script zsh', invoke=False)
    assert ' foo' in stdout

def binary_names_can_be_given_directly(self):
    program = Program(binary_names=['foo', 'bar'])
    (stdout, _) = run('foo --print-completion-script zsh', invoke=False, program=program)
    assert ' foo bar' in stdout

def print_version_displays_name_and_version(self):
    expect('--version', program=Program(name='MyProgram', version='0.1.0'), out='MyProgram 0.1.0\n')

def initial_context_contains_truly_core_arguments_regardless_of_namespace_value(self):
    for program in (Program(), Program(namespace=Collection())):
        for arg in ('--complete', '--debug', '--warn-only', '--list'):
            (stdout, _) = run('--help', program=program)
            assert arg in stdout

def initial_context_null_namespace_triggers_task_related_args(self):
    program = Program(namespace=None)
    for arg in program.task_args():
        (stdout, _) = run('--help', program=program)
        assert arg.name in stdout

def initial_context_non_null_namespace_does_not_trigger_task_related_args(self):
    for arg in Program().task_args():
        program = Program(namespace=Collection(mytask=Task(Mock())))
        (stdout, _) = run('--help', program=program)
        assert arg.name not in stdout

def load_collection_complains_when_default_collection_not_found(self):
    with cd(ROOT):
        expect('-l', err="Can't find any collection named 'tasks'!\n")

def load_collection_complains_when_explicit_collection_not_found(self):
    expect('-c huhwhat -l', err="Can't find any collection named 'huhwhat'!\n")

@trap
def load_collection_uses_loader_class_given(self):
    klass = Mock(side_effect=FilesystemLoader)
    Program(loader_class=klass).run('myapp --help foo', exit=False)
    klass.assert_called_with(start=ANY, config=ANY)

def execute_uses_executor_class_given(self):
    klass = Mock()
    Program(executor_class=klass).run('myapp foo', exit=False)
    klass.assert_called_with(ANY, ANY, ANY)
    klass.return_value.execute.assert_called_with(ANY)

def execute_executor_class_may_be_overridden_via_configured_string(self):

    class ExecutorOverridingConfig(Config):

        @staticmethod
        def global_defaults():
            defaults = Config.global_defaults()
            path = 'custom_executor.CustomExecutor'
            merge_dicts(defaults, {'tasks': {'executor_class': path}})
            return defaults
    mock = load('custom_executor').CustomExecutor
    p = Program(config_class=ExecutorOverridingConfig)
    p.run('myapp noop', exit=False)
    assert mock.assert_called
    assert mock.return_value.execute.called

def execute_executor_is_given_access_to_core_args_and_remainder(self):
    klass = Mock()
    cmd = 'myapp -e foo -- myremainder'
    Program(executor_class=klass).run(cmd, exit=False)
    core = klass.call_args[0][2]
    assert core[0].args['echo'].value
    assert core.remainder == 'myremainder'

def core_args_returns_core_args_list(self):
    core_args = Program().core_args()
    core_arg_names = [x.names[0] for x in core_args]
    for name in ('complete', 'help', 'pty', 'version'):
        assert name in core_arg_names
    assert isinstance(core_args, list)

def args_property_shorthand_for_self_core_args(self):
    """is shorthand for self.core[0].args"""
    p = Program()
    p.run('myapp -e noop', exit=False)
    args = p.args
    assert isinstance(args, Lexicon)
    assert args.echo.value is True

def core_args_from_task_contexts_core_context_gets_updated_with_core_flags_from_tasks(self):
    p = Program()
    p.run('myapp -e noop --hide both', exit=False)
    assert p.args.echo.value is True
    assert p.args.hide.value == 'both'

def core_args_from_task_contexts_copying_from_task_context_does_not_set_empty_list_values(self):
    p = Program()

    def filename_args():
        return [Argument('filename', kind=list)]
    p.core = ParseResult([ParserContext(args=filename_args())])
    p.core_via_tasks = ParserContext(args=filename_args())
    assert p.args['filename'].value == []

def core_args_from_task_contexts_copying_from_task_context_does_not_overwrite_good_values(self):

    def make_arg():
        return Argument('filename', kind=list)
    p = Program()
    arg = make_arg()
    arg.value = 'some-file'
    p.core = ParseResult([ParserContext(args=[arg])])
    p.core_via_tasks = ParserContext(args=[make_arg()])
    assert p.args.filename.value == ['some-file']

def run_seeks_and_loads_tasks_module_by_default(self):
    expect('foo', out='Hm\n')

def run_does_not_seek_tasks_module_if_namespace_was_given(self):
    expect('foo', err="No idea what 'foo' is!\n", program=Program(namespace=Collection('blank')))

def run_explicit_namespace_works_correctly(self):
    ns = Collection.from_module(load('integration'))
    expect('print-foo', out='foo\n', program=Program(namespace=ns))

def run_allows_explicit_task_module_specification(self):
    expect('-c integration print-foo', out='foo\n')

def run_handles_task_arguments(self):
    expect('-c integration print-name --name inigo', out='inigo\n')

def run_can_change_collection_search_root(self):
    for flag in ('-r', '--search-root'):
        expect('{} branch/ alt-root'.format(flag), out='Down with the alt-root!\n')

def run_can_change_collection_search_root_with_explicit_module_name(self):
    for flag in ('-r', '--search-root'):
        expect('{} branch/ -c explicit lyrics'.format(flag), out="Don't swear!\n")

@trap
@patch('invoke.program.sys.exit')
def run_ParseErrors_display_message_and_exit_1(self, mock_exit):
    p = Program()
    nah = 'nopenotvalidsorry'
    p.run('myapp {}'.format(nah))
    stderr = sys.stderr.getvalue()
    assert stderr == "No idea what '{}' is!\n".format(nah)
    mock_exit.assert_called_with(1)

@trap
@patch('invoke.program.sys.exit')
def run_UnexpectedExit_exits_with_code_when_no_hiding(self, mock_exit):
    p = Program()
    oops = UnexpectedExit(Result(command='meh', exited=17, hide=tuple()))
    p.execute = Mock(side_effect=oops)
    p.run('myapp foo')
    assert sys.stderr.getvalue() == ''
    mock_exit.assert_called_with(17)

@trap
@patch('invoke.program.sys.exit')
def run_shows_UnexpectedExit_str_when_streams_hidden(self, mock_exit):
    p = Program()
    oops = UnexpectedExit(Result(command='meh', exited=54, stdout='things!', stderr='ohnoz!', encoding='utf-8', hide=('stdout', 'stderr')))
    p.execute = Mock(side_effect=oops)
    p.run('myapp foo')
    stderr = sys.stderr.getvalue()
    expected = "Encountered a bad command exit code!\n\nCommand: 'meh'\n\nExit code: 54\n\nStdout:\n\nthings!\n\nStderr:\n\nohnoz!\n\n"
    assert stderr == expected
    mock_exit.assert_called_with(54)

@trap
@patch('invoke.program.sys.exit')
def run_UnexpectedExit_str_encodes_stdout_and_err(self, mock_exit):
    p = Program()
    oops = UnexpectedExit(Result(command='meh', exited=54, stdout=u'this is not ascii: ሴ', stderr=u'this is also not ascii: 䌡', encoding='utf-8', hide=('stdout', 'stderr')))
    p.execute = Mock(side_effect=oops)
    p.run('myapp foo')
    expected = b"Encountered a bad command exit code!\n\nCommand: 'meh'\n\nExit code: 54\n\nStdout:\n\nthis is not ascii: \xe1\x88\xb4\n\nStderr:\n\nthis is also not ascii: \xe4\x8c\xa1\n\n"
    got = six.BytesIO.getvalue(sys.stderr)
    assert got == expected

def run_should_show_core_usage_on_core_parse_failures(self):
    skip()

def run_should_show_context_usage_on_context_parse_failures(self):
    skip()

@trap
@patch('invoke.program.sys.exit')
def run_turns_KeyboardInterrupt_into_exit_code_1(self, mock_exit):
    p = Program()
    p.execute = Mock(side_effect=KeyboardInterrupt)
    p.run('myapp -c foo mytask')
    mock_exit.assert_called_with(1)

def core_empty_invocation_with_no_default_task_prints_help(self):
    (stdout, _) = run('-c foo')
    assert 'Core options:' in stdout

@skip_if_windows
def core_core_help_option_prints_core_help(self):
    expected = "\nUsage: inv[oke] [--core-opts] task1 [--task1-opts] ... taskN [--taskN-opts]\n\nCore options:\n\n  --complete                         Print tab-completion candidates for given\n                                     parse remainder.\n  --hide=STRING                      Set default value of run()'s 'hide' kwarg.\n  --no-dedupe                        Disable task deduplication.\n  --print-completion-script=STRING   Print the tab-completion script for your\n                                     preferred shell (bash|zsh|fish).\n  --prompt-for-sudo-password         Prompt user at start of session for the\n                                     sudo.password config value.\n  --write-pyc                        Enable creation of .pyc files.\n  -c STRING, --collection=STRING     Specify collection name to load.\n  -d, --debug                        Enable debug output.\n  -D INT, --list-depth=INT           When listing tasks, only show the first\n                                     INT levels.\n  -e, --echo                         Echo executed commands before running.\n  -f STRING, --config=STRING         Runtime configuration file to use.\n  -F STRING, --list-format=STRING    Change the display format used when\n                                     listing tasks. Should be one of: flat\n                                     (default), nested, json.\n  -h [STRING], --help[=STRING]       Show core or per-task help and exit.\n  -l [STRING], --list[=STRING]       List available tasks, optionally limited\n                                     to a namespace.\n  -p, --pty                          Use a pty when executing shell commands.\n  -r STRING, --search-root=STRING    Change root directory used for finding\n                                     task modules.\n  -R, --dry                          Echo commands instead of running.\n  -T INT, --command-timeout=INT      Specify a global command execution\n                                     timeout, in seconds.\n  -V, --version                      Show version and exit.\n  -w, --warn-only                    Warn, instead of failing, when shell\n                                     commands fail.\n\n".lstrip()
    for flag in ['-h', '--help']:
        expect(flag, out=expected, program=main.program)

def core_bundled_namespace_help_includes_subcommand_listing(self):
    (t1, t2) = (Task(Mock()), Task(Mock()))
    coll = Collection(task1=t1, task2=t2)
    p = Program(namespace=coll)
    for expected in ('Usage: myapp [--core-opts] <subcommand> [--subcommand-opts] ...\n', 'Core options:\n', '--echo', 'Subcommands:\n', '  task1', '  task2'):
        (stdout, _) = run('myapp --help', program=p, invoke=False)
        assert expected in stdout

def core_core_help_doesnt_get_mad_if_loading_fails(self):
    with cd(ROOT):
        (stdout, _) = run('--help')
        assert 'Usage: ' in stdout

def per_task_prints_help_for_task_only(self):
    expected = '\nUsage: invoke [--core-opts] punch [--options] [other tasks here ...]\n\nDocstring:\n  none\n\nOptions:\n  -h STRING, --why=STRING   Motive\n  -w STRING, --who=STRING   Who to punch\n\n'.lstrip()
    for flag in ['-h', '--help']:
        expect('-c decorators {} punch'.format(flag), out=expected)

def per_task_works_for_unparameterized_tasks(self):
    expected = '\nUsage: invoke [--core-opts] biz [other tasks here ...]\n\nDocstring:\n  none\n\nOptions:\n  none\n\n'.lstrip()
    expect('-c decorators -h biz', out=expected)

def per_task_honors_program_binary(self):
    (stdout, _) = run('-c decorators -h biz', program=Program(binary='notinvoke'))
    assert 'Usage: notinvoke' in stdout

def per_task_displays_docstrings_if_given(self):
    expected = '\nUsage: invoke [--core-opts] foo [other tasks here ...]\n\nDocstring:\n  Foo the bar.\n\nOptions:\n  none\n\n'.lstrip()
    expect('-c decorators -h foo', out=expected)

def per_task_dedents_correctly(self):
    expected = '\nUsage: invoke [--core-opts] foo2 [other tasks here ...]\n\nDocstring:\n  Foo the bar:\n\n    example code\n\n  Added in 1.0\n\nOptions:\n  none\n\n'.lstrip()
    expect('-c decorators -h foo2', out=expected)

def per_task_dedents_correctly_for_alt_docstring_style(self):
    expected = '\nUsage: invoke [--core-opts] foo3 [other tasks here ...]\n\nDocstring:\n  Foo the other bar:\n\n    example code\n\n  Added in 1.1\n\nOptions:\n  none\n\n'.lstrip()
    expect('-c decorators -h foo3', out=expected)

def per_task_exits_after_printing(self):
    expected = '\nUsage: invoke [--core-opts] punch [--options] [other tasks here ...]\n\nDocstring:\n  none\n\nOptions:\n  -h STRING, --why=STRING   Motive\n  -w STRING, --who=STRING   Who to punch\n\n'.lstrip()
    expect('-c decorators -h punch --list', out=expected)

def per_task_complains_if_given_invalid_task_name(self):
    expect('-h this', err="No idea what 'this' is!\n")

def task_list__listing(self, lines):
    return '\nAvailable tasks:\n\n{}\n\n'.format('\n'.join(('  ' + x for x in lines))).lstrip()

def task_list__list_eq(self, collection, listing):
    cmd = '-c {} --list'.format(collection)
    expect(cmd, out=self._listing(listing))

def task_list_simple_output(self):
    expected = self._listing(('bar', 'biz', 'boz', 'foo', 'post1', 'post2', 'print-foo', 'print-name', 'print-underscored-arg'))
    for flag in ('-l', '--list'):
        expect('-c integration {}'.format(flag), out=expected)

def task_list_namespacing(self):
    self._list_eq('namespacing', ('toplevel', 'module.mytask'))

def task_list_top_level_tasks_listed_first(self):
    self._list_eq('simple_ns_list', ('z-toplevel', 'a.b.subtask'))

def task_list_aliases_sorted_alphabetically(self):
    self._list_eq('alias_sorting', ('toplevel (a, z)',))

def task_list_default_tasks(self):
    self._list_eq('explicit_root', ('top-level (other-top)', 'sub-level.sub-task (sub-level, sub-level.other-sub)'))

def task_list_docstrings_shown_alongside(self):
    self._list_eq('docstrings', ('leading-whitespace    foo', 'no-docstring', 'one-line              foo', 'two-lines             foo', 'with-aliases (a, b)   foo'))

def task_list_docstrings_are_wrapped_to_terminal_width(self):
    self._list_eq('nontrivial_docstrings', ('no-docstring', 'task-one       Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n                 Nullam id dictum', 'task-two       Nulla eget ultrices ante. Curabitur sagittis commodo posuere.\n                 Duis dapibus'))

def task_list_empty_collections_say_no_tasks(self):
    expect('-c empty -l', err="No tasks found in collection 'empty'!\n")

def task_list_nontrivial_trees_are_sorted_by_namespace_and_depth(self):
    expected = 'Available tasks:\n\n  shell (ipython)                       Load a REPL with project state already\n                                        set up.\n  test (run-tests)                      Run the test suite with baked-in args.\n  build.all (build, build.everything)   Build all necessary artifacts.\n  build.c-ext (build.ext)               Build our internal C extension.\n  build.zap                             A silly way to clean.\n  build.docs.all (build.docs)           Build all doc formats.\n  build.docs.html                       Build HTML output only.\n  build.docs.pdf                        Build PDF output only.\n  build.python.all (build.python)       Build all Python packages.\n  build.python.sdist                    Build classic style tar.gz.\n  build.python.wheel                    Build a wheel.\n  deploy.db (deploy.db-servers)         Deploy to our database servers.\n  deploy.everywhere (deploy)            Deploy to all targets.\n  deploy.web                            Update and bounce the webservers.\n  provision.db                          Stand up one or more DB servers.\n  provision.web                         Stand up a Web server.\n\nDefault task: test\n\n'
    (stdout, _) = run('-c tree --list')
    assert expected == stdout

def namespace_limiting_argument_limits_display_to_given_namespace(self):
    (stdout, _) = run('-c tree --list build')
    expected = "Available 'build' tasks:\n\n  .all (.everything)      Build all necessary artifacts.\n  .c-ext (.ext)           Build our internal C extension.\n  .zap                    A silly way to clean.\n  .docs.all (.docs)       Build all doc formats.\n  .docs.html              Build HTML output only.\n  .docs.pdf               Build PDF output only.\n  .python.all (.python)   Build all Python packages.\n  .python.sdist           Build classic style tar.gz.\n  .python.wheel           Build a wheel.\n\nDefault 'build' task: .all\n\n"
    assert expected == stdout

def namespace_limiting_argument_may_be_a_nested_namespace(self):
    (stdout, _) = run('-c tree --list build.docs')
    expected = "Available 'build.docs' tasks:\n\n  .all    Build all doc formats.\n  .html   Build HTML output only.\n  .pdf    Build PDF output only.\n\nDefault 'build.docs' task: .all\n\n"
    assert expected == stdout

def namespace_limiting_empty_namespaces_say_no_tasks_in_namespace(self):
    expect('-c empty_subcollection -l subcollection', err="No tasks found in collection 'subcollection'!\n")

def namespace_limiting_invalid_namespaces_exit_with_message(self):
    expect('-c empty -l nope', err="Sub-collection 'nope' not found!\n")

def depth_limiting_limits_display_to_given_depth(self):
    expected = 'Available tasks (depth=1):\n\n  shell (ipython)                  Load a REPL with project state already set\n                                   up.\n  test (run-tests)                 Run the test suite with baked-in args.\n  build [3 tasks, 2 collections]   Tasks for compiling static code and assets.\n  deploy [3 tasks]                 How to deploy our code and configs.\n  provision [2 tasks]              System setup code.\n\nDefault task: test\n\n'
    (stdout, _) = run('-c tree --list -F flat --list-depth 1')
    assert expected == stdout

def depth_limiting_non_base_case(self):
    expected = 'Available tasks (depth=2):\n\n  shell (ipython)                       Load a REPL with project state already\n                                        set up.\n  test (run-tests)                      Run the test suite with baked-in args.\n  build.all (build, build.everything)   Build all necessary artifacts.\n  build.c-ext (build.ext)               Build our internal C extension.\n  build.zap                             A silly way to clean.\n  build.docs [3 tasks]                  Tasks for managing Sphinx docs.\n  build.python [3 tasks]                PyPI/etc distribution artifacts.\n  deploy.db (deploy.db-servers)         Deploy to our database servers.\n  deploy.everywhere (deploy)            Deploy to all targets.\n  deploy.web                            Update and bounce the webservers.\n  provision.db                          Stand up one or more DB servers.\n  provision.web                         Stand up a Web server.\n\nDefault task: test\n\n'
    (stdout, _) = run('-c tree --list --list-depth=2')
    assert expected == stdout

def depth_limiting_depth_can_be_deeper_than_real_depth(self):
    expected = 'Available tasks (depth=5):\n\n  shell (ipython)                       Load a REPL with project state already\n                                        set up.\n  test (run-tests)                      Run the test suite with baked-in args.\n  build.all (build, build.everything)   Build all necessary artifacts.\n  build.c-ext (build.ext)               Build our internal C extension.\n  build.zap                             A silly way to clean.\n  build.docs.all (build.docs)           Build all doc formats.\n  build.docs.html                       Build HTML output only.\n  build.docs.pdf                        Build PDF output only.\n  build.python.all (build.python)       Build all Python packages.\n  build.python.sdist                    Build classic style tar.gz.\n  build.python.wheel                    Build a wheel.\n  deploy.db (deploy.db-servers)         Deploy to our database servers.\n  deploy.everywhere (deploy)            Deploy to all targets.\n  deploy.web                            Update and bounce the webservers.\n  provision.db                          Stand up one or more DB servers.\n  provision.web                         Stand up a Web server.\n\nDefault task: test\n\n'
    (stdout, _) = run('-c tree --list --list-depth=5')
    assert expected == stdout

def depth_limiting_works_with_explicit_namespace(self):
    expected = "Available 'build' tasks (depth=1):\n\n  .all (.everything)   Build all necessary artifacts.\n  .c-ext (.ext)        Build our internal C extension.\n  .zap                 A silly way to clean.\n  .docs [3 tasks]      Tasks for managing Sphinx docs.\n  .python [3 tasks]    PyPI/etc distribution artifacts.\n\nDefault 'build' task: .all\n\n"
    (stdout, _) = run('-c tree --list build --list-depth=1')
    assert expected == stdout

def depth_limiting_short_flag_is_D(self):
    expected = 'Available tasks (depth=1):\n\n  shell (ipython)                  Load a REPL with project state already set\n                                   up.\n  test (run-tests)                 Run the test suite with baked-in args.\n  build [3 tasks, 2 collections]   Tasks for compiling static code and assets.\n  deploy [3 tasks]                 How to deploy our code and configs.\n  provision [2 tasks]              System setup code.\n\nDefault task: test\n\n'
    (stdout, _) = run('-c tree --list --list-format=flat -D 1')
    assert expected == stdout

def depth_limiting_depth_of_zero_is_same_as_max_depth(self):
    expected = 'Available tasks:\n\n  shell (ipython)                       Load a REPL with project state already\n                                        set up.\n  test (run-tests)                      Run the test suite with baked-in args.\n  build.all (build, build.everything)   Build all necessary artifacts.\n  build.c-ext (build.ext)               Build our internal C extension.\n  build.zap                             A silly way to clean.\n  build.docs.all (build.docs)           Build all doc formats.\n  build.docs.html                       Build HTML output only.\n  build.docs.pdf                        Build PDF output only.\n  build.python.all (build.python)       Build all Python packages.\n  build.python.sdist                    Build classic style tar.gz.\n  build.python.wheel                    Build a wheel.\n  deploy.db (deploy.db-servers)         Deploy to our database servers.\n  deploy.everywhere (deploy)            Deploy to all targets.\n  deploy.web                            Update and bounce the webservers.\n  provision.db                          Stand up one or more DB servers.\n  provision.web                         Stand up a Web server.\n\nDefault task: test\n\n'
    (stdout, _) = run('-c tree --list --list-format=flat -D 0')
    assert expected == stdout

def format_flat_is_legacy_default_format(self):
    expected = 'Available tasks:\n\n  shell (ipython)                       Load a REPL with project state already\n                                        set up.\n  test (run-tests)                      Run the test suite with baked-in args.\n  build.all (build, build.everything)   Build all necessary artifacts.\n  build.c-ext (build.ext)               Build our internal C extension.\n  build.zap                             A silly way to clean.\n  build.docs.all (build.docs)           Build all doc formats.\n  build.docs.html                       Build HTML output only.\n  build.docs.pdf                        Build PDF output only.\n  build.python.all (build.python)       Build all Python packages.\n  build.python.sdist                    Build classic style tar.gz.\n  build.python.wheel                    Build a wheel.\n  deploy.db (deploy.db-servers)         Deploy to our database servers.\n  deploy.everywhere (deploy)            Deploy to all targets.\n  deploy.web                            Update and bounce the webservers.\n  provision.db                          Stand up one or more DB servers.\n  provision.web                         Stand up a Web server.\n\nDefault task: test\n\n'
    (stdout, _) = run('-c tree --list --list-format=flat')
    assert expected == stdout

def nested_base_case(self):
    expected = "Available tasks ('*' denotes collection defaults):\n\n  shell (ipython)           Load a REPL with project state already set up.\n  test* (run-tests)         Run the test suite with baked-in args.\n  build                     Tasks for compiling static code and assets.\n      .all* (.everything)   Build all necessary artifacts.\n      .c-ext (.ext)         Build our internal C extension.\n      .zap                  A silly way to clean.\n      .docs                 Tasks for managing Sphinx docs.\n          .all*             Build all doc formats.\n          .html             Build HTML output only.\n          .pdf              Build PDF output only.\n      .python               PyPI/etc distribution artifacts.\n          .all*             Build all Python packages.\n          .sdist            Build classic style tar.gz.\n          .wheel            Build a wheel.\n  deploy                    How to deploy our code and configs.\n      .db (.db-servers)     Deploy to our database servers.\n      .everywhere*          Deploy to all targets.\n      .web                  Update and bounce the webservers.\n  provision                 System setup code.\n      .db                   Stand up one or more DB servers.\n      .web                  Stand up a Web server.\n\nDefault task: test\n\n"
    (stdout, _) = run('-c tree -l -F nested')
    assert expected == stdout

def nested_honors_namespace_arg_to_list(self):
    (stdout, _) = run('-c tree --list build -F nested')
    expected = "Available 'build' tasks ('*' denotes collection defaults):\n\n  .all* (.everything)   Build all necessary artifacts.\n  .c-ext (.ext)         Build our internal C extension.\n  .zap                  A silly way to clean.\n  .docs                 Tasks for managing Sphinx docs.\n      .all*             Build all doc formats.\n      .html             Build HTML output only.\n      .pdf              Build PDF output only.\n  .python               PyPI/etc distribution artifacts.\n      .all*             Build all Python packages.\n      .sdist            Build classic style tar.gz.\n      .wheel            Build a wheel.\n\nDefault 'build' task: .all\n\n"
    assert expected == stdout

def nested_honors_depth_arg(self):
    expected = "Available tasks (depth=2; '*' denotes collection defaults):\n\n  shell (ipython)           Load a REPL with project state already set up.\n  test* (run-tests)         Run the test suite with baked-in args.\n  build                     Tasks for compiling static code and assets.\n      .all* (.everything)   Build all necessary artifacts.\n      .c-ext (.ext)         Build our internal C extension.\n      .zap                  A silly way to clean.\n      .docs [3 tasks]       Tasks for managing Sphinx docs.\n      .python [3 tasks]     PyPI/etc distribution artifacts.\n  deploy                    How to deploy our code and configs.\n      .db (.db-servers)     Deploy to our database servers.\n      .everywhere*          Deploy to all targets.\n      .web                  Update and bounce the webservers.\n  provision                 System setup code.\n      .db                   Stand up one or more DB servers.\n      .web                  Stand up a Web server.\n\nDefault task: test\n\n"
    (stdout, _) = run('-c tree -l -F nested --list-depth 2')
    assert expected == stdout

def nested_depth_arg_deeper_than_real_depth(self):
    expected = "Available tasks (depth=5; '*' denotes collection defaults):\n\n  shell (ipython)           Load a REPL with project state already set up.\n  test* (run-tests)         Run the test suite with baked-in args.\n  build                     Tasks for compiling static code and assets.\n      .all* (.everything)   Build all necessary artifacts.\n      .c-ext (.ext)         Build our internal C extension.\n      .zap                  A silly way to clean.\n      .docs                 Tasks for managing Sphinx docs.\n          .all*             Build all doc formats.\n          .html             Build HTML output only.\n          .pdf              Build PDF output only.\n      .python               PyPI/etc distribution artifacts.\n          .all*             Build all Python packages.\n          .sdist            Build classic style tar.gz.\n          .wheel            Build a wheel.\n  deploy                    How to deploy our code and configs.\n      .db (.db-servers)     Deploy to our database servers.\n      .everywhere*          Deploy to all targets.\n      .web                  Update and bounce the webservers.\n  provision                 System setup code.\n      .db                   Stand up one or more DB servers.\n      .web                  Stand up a Web server.\n\nDefault task: test\n\n"
    (stdout, _) = run('-c tree -l -F nested --list-depth 5')
    assert expected == stdout

def nested_all_possible_options(self):
    expected = "Available 'build' tasks (depth=1; '*' denotes collection defaults):\n\n  .all* (.everything)   Build all necessary artifacts.\n  .c-ext (.ext)         Build our internal C extension.\n  .zap                  A silly way to clean.\n  .docs [3 tasks]       Tasks for managing Sphinx docs.\n  .python [3 tasks]     PyPI/etc distribution artifacts.\n\nDefault 'build' task: .all\n\n"
    (stdout, _) = run('-c tree -l build -F nested -D1')
    assert expected == stdout

def nested_empty_namespaces_say_no_tasks_in_namespace(self):
    expect('-c empty_subcollection -l subcollection -F nested', err="No tasks found in collection 'subcollection'!\n")

def nested_invalid_namespaces_exit_with_message(self):
    expect('-c empty -l nope -F nested', err="Sub-collection 'nope' not found!\n")

def json_setup(self):
    self.tree = json.loads(support_file('tree.json'))
    self.by_name = {x['name']: x for x in self.tree['collections']}

def json_base_case(self):
    (stdout, _) = run('-c tree --list --list-format=json')
    assert self.tree == json.loads(stdout)

def json_honors_namespace_arg_to_list(self):
    (stdout, _) = run('-c tree --list deploy --list-format=json')
    expected = self.by_name['deploy']
    assert expected == json.loads(stdout)

def json_does_not_honor_depth_arg(self):
    (_, stderr) = run('-c tree -l --list-format json -D 2')
    expected = 'The --list-depth option is not supported with JSON format!\n'
    assert expected == stderr

def json_does_not_honor_depth_arg_even_with_namespace(self):
    (_, stderr) = run('-c tree -l build -F json -D 2')
    expected = 'The --list-depth option is not supported with JSON format!\n'
    assert expected == stderr

def json_empty_namespaces_say_no_tasks_in_namespace(self):
    expect('-c empty_subcollection -l subcollection -F nested', err="No tasks found in collection 'subcollection'!\n")

def json_invalid_namespaces_exit_with_message(self):
    expect('-c empty -l nope -F nested', err="Sub-collection 'nope' not found!\n")

def run_options__test_flag(self, flag, key, value=True):
    p = Program()
    p.execute = Mock()
    p.run('inv {} foo'.format(flag))
    assert p.config.run[key] == value

def run_options_warn_only(self):
    self._test_flag('-w', 'warn')

def run_options_pty(self):
    self._test_flag('-p', 'pty')

def run_options_hide(self):
    self._test_flag('--hide both', 'hide', value='both')

def run_options_echo(self):
    self._test_flag('-e', 'echo')

def run_options_timeout(self):
    for flag in ('-T', '--command-timeout'):
        p = Program()
        p.execute = Mock()
        p.run('inv {} 5 foo'.format(flag))
        assert p.config.timeouts.command == 5

def configuration__klass(self):
    instance_mock = Mock(tasks=Mock(collection_name='whatever', search_root='meh'))
    return Mock(return_value=instance_mock)

@trap
def configuration_config_class_init_kwarg_is_honored(self):
    klass = self._klass()
    Program(config_class=klass).run('myapp foo', exit=False)
    assert len(klass.call_args_list) == 1

@trap
def configuration_config_attribute_is_memoized(self):
    klass = self._klass()
    p = Program(config_class=klass)
    p.run('myapp foo', exit=False)
    assert klass.call_count == 1
    p.config
    assert klass.call_count == 1

def configuration_per_project_config_files_are_loaded_before_task_parsing(self):
    with cd(os.path.join('configs', 'underscores')):
        expect('i_have_underscores')

def configuration_per_project_config_files_load_with_explicit_ns(self):
    with cd(os.path.join('configs', 'yaml')):
        expect('-c explicit mytask')

def runtime_config_file_can_be_set_via_cli_option(self):
    with cd('configs'):
        expect('-c runtime -f yaml/invoke.yaml mytask')

def runtime_config_file_can_be_set_via_env(self, reset_environ):
    os.environ['INVOKE_RUNTIME_CONFIG'] = 'yaml/invoke.yaml'
    with cd('configs'):
        expect('-c runtime mytask')

def runtime_config_file_cli_option_wins_over_env(self, reset_environ):
    os.environ['INVOKE_RUNTIME_CONFIG'] = 'json/invoke.json'
    with cd('configs'):
        expect('-c runtime -f yaml/invoke.yaml mytask')

def configuration_tasks_dedupe_honors_configuration(self):
    with cd('configs'):
        expect('-c integration -f no-dedupe.yaml biz', out='\nfoo\nfoo\nbar\nbiz\npost1\npost2\npost2\n'.lstrip())
        expect('-c integration -f dedupe.yaml --no-dedupe biz', out='\nfoo\nfoo\nbar\nbiz\npost1\npost2\npost2\n'.lstrip())

def configuration_env_vars_load_with_prefix(self, monkeypatch):
    monkeypatch.setenv('INVOKE_RUN_ECHO', '1')
    expect('-c contextualized check-echo')

def configuration_env_var_prefix_can_be_overridden(self, monkeypatch):
    monkeypatch.setenv('MYAPP_RUN_HIDE', 'both')

    class MyConf(Config):
        env_prefix = 'MYAPP'
    p = Program(config_class=MyConf)
    p.run('inv -c contextualized check-hide')

@patch('invoke.program.getpass.getpass')
def other_behavior_sudo_prompt_up_front(self, getpass):
    getpass.return_value = 'mypassword'
    with support_path():
        try:
            Program().run('inv --prompt-for-sudo-password -c sudo_prompt expect-config')
        except SystemExit as e:
            assert e.code == 0
    prompt = "Desired 'sudo.password' config value: "
    getpass.assert_called_once_with(prompt)