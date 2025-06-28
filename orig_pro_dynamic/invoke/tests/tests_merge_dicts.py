from pytest import raises
from invoke.config import merge_dicts, copy_dict, AmbiguousMergeError

def merge_dicts__merging_data_onto_empty_dict(self):
    d1 = {}
    d2 = {'foo': 'bar'}
    merge_dicts(d1, d2)
    assert d1 == d2

def merge_dicts__updating_with_None_acts_like_merging_empty_dict(self):
    d1 = {'my': 'data'}
    d2 = None
    merge_dicts(d1, d2)
    assert d1 == {'my': 'data'}

def merge_dicts__orthogonal_data_merges(self):
    d1 = {'foo': 'bar'}
    d2 = {'biz': 'baz'}
    merge_dicts(d1, d2)
    assert d1 == {'foo': 'bar', 'biz': 'baz'}

def merge_dicts__updates_arg_values_win(self):
    d1 = {'foo': 'bar'}
    d2 = {'foo': 'notbar'}
    merge_dicts(d1, d2)
    assert d1 == {'foo': 'notbar'}

def merge_dicts__non_dict_type_mismatch_overwrites_ok(self):
    d1 = {'foo': 'bar'}
    d2 = {'foo': [1, 2, 3]}
    merge_dicts(d1, d2)
    assert d1 == {'foo': [1, 2, 3]}

def merge_dicts__merging_dict_into_nondict_raises_error(self):
    d1 = {'foo': 'bar'}
    d2 = {'foo': {'uh': 'oh'}}
    with raises(AmbiguousMergeError):
        merge_dicts(d1, d2)

def merge_dicts__merging_nondict_into_dict_raises_error(self):
    d1 = {'foo': {'uh': 'oh'}}
    d2 = {'foo': 'bar'}
    with raises(AmbiguousMergeError):
        merge_dicts(d1, d2)

def merge_dicts__nested_leaf_values_merge_ok(self):
    d1 = {'foo': {'bar': {'biz': 'baz'}}}
    d2 = {'foo': {'bar': {'biz': 'notbaz'}}}
    merge_dicts(d1, d2)
    assert d1 == {'foo': {'bar': {'biz': 'notbaz'}}}

def merge_dicts__mixed_branch_levels_merges_ok(self):
    d1 = {'foo': {'bar': {'biz': 'baz'}}, 'meh': 17, 'myown': 'ok'}
    d2 = {'foo': {'bar': {'biz': 'notbaz'}}, 'meh': 25}
    merge_dicts(d1, d2)
    expected = {'foo': {'bar': {'biz': 'notbaz'}}, 'meh': 25, 'myown': 'ok'}
    assert d1 == expected

def merge_dicts__dict_value_merges_are_not_references(self):
    core = {}
    coll = {'foo': {'bar': {'biz': 'coll value'}}}
    proj = {'foo': {'bar': {'biz': 'proj value'}}}
    merge_dicts(core, proj)
    assert core == {'foo': {'bar': {'biz': 'proj value'}}}
    assert proj['foo']['bar']['biz'] == 'proj value'
    assert core['foo'] is not proj['foo'], 'Core foo is literally proj foo!'
    merge_dicts(core, proj)
    assert core == {'foo': {'bar': {'biz': 'proj value'}}}
    assert proj['foo']['bar']['biz'] == 'proj value'
    merge_dicts(core, coll)
    assert core == {'foo': {'bar': {'biz': 'coll value'}}}
    assert proj['foo']['bar']['biz'] == 'proj value'

def merge_dicts__merge_file_types_by_reference(self):
    with open(__file__) as fd:
        d1 = {}
        d2 = {'foo': fd}
        merge_dicts(d1, d2)
        assert d1['foo'].closed is False

def copy_dict__returns_deep_copy_of_given_dict(self):
    source = {'foo': {'bar': {'biz': 'baz'}}}
    copy = copy_dict(source)
    assert copy['foo']['bar'] == source['foo']['bar']
    assert copy['foo']['bar'] is not source['foo']['bar']
    copy['foo']['bar']['biz'] = 'notbaz'
    assert source['foo']['bar']['biz'] == 'baz'