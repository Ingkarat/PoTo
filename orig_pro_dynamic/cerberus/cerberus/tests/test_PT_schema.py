from cerberus import schema

def test_PT_update():
    vs = schema.ValidatedSchema()
    sch = {'sub_dict': {'type': 'dict', 'schema': {'foo': {'type': 'string'}}}}
    vs.update(sch)