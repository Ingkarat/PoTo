import ast
import pickle
import os

import pt_engine.datatypes as datatypes

from .utils.graph import Graph
from .utils.base import ins, is_constant, is_universal_constant, encode_constant, decode_constant, cast_proto_container
from .solvers.call_stmt_solver import CallStmt

pt_graph = Graph()
call_graph = Graph()
mirror_call_graph = Graph() # Currently unused

# a mapping from variable to enclosing function def
var_to_encl_func = {}

fresh_id = 0

def fresh_var(encl_func = None):
    global fresh_id
    fresh_id += 1
    if encl_func != None:
        var_to_encl_func["v_"+str(fresh_id)] = encl_func
    return fresh_id

obj_id = 0

def fresh_obj():
    global obj_id
    obj_id += 1
    return obj_id


# Note: meta objects are functions, classes, etc
# Invariant: var_id points to the corresponding obj_id
# Invariant: vars.keys == meta_objects.keys
# vars is a map from "full name of Globally Visible meta object" -> var_id
vars = {}
# meta_obejcts is a map from full name of GLOBALLY VISSIBLE meta object -> obj_id
meta_objects = {}


# obj_id -> Object
objects = {}
# obj_id -> encl_path (module:class:function)
obj_id_to_encl = {}

# Full package name -> Module 
package_env = {}


# Procedures with effects on global state

def get_var_id(full_var_name):
    global vars
    global fresh_id
    if full_var_name not in vars:
        fresh_id = fresh_var()
        var = "v_"+str(fresh_id)
        vars[full_var_name] = var
        #print("In get var id: ",full_var_name, var)
    return vars[full_var_name]    

def get_meta_obj_id(full_meta_obj_name):
    global meta_objects
    global obj_id
    if full_meta_obj_name not in meta_objects:
        obj_id = fresh_obj()
        obj = "o_"+str(obj_id)
        meta_objects[full_meta_obj_name] = obj
    return meta_objects[full_meta_obj_name]

def register_meta_object(full_var_name,node):   
    var_id = get_var_id(full_var_name)
    meta_obj_id = get_meta_obj_id(full_var_name)
    encl_module_name = full_var_name.split(':')[0]
    if meta_obj_id not in objects:
        assert ins(node,ast.FunctionDef) or ins(node,ast.ClassDef) or ins(node,ast.AsyncFunctionDef)
        if ins(node,ast.FunctionDef) or ins(node,ast.AsyncFunctionDef): 
            objects[meta_obj_id] = datatypes.Object("meta_func",func=node,module_name=encl_module_name)
        else:
            objects[meta_obj_id] = datatypes.Object("meta_cls",cls=node,module_name=encl_module_name)
        pt_graph.addEdge(var_id,meta_obj_id,"")    
    return var_id 

# Creates a new prototype object
def new_proto(module_name,lhs,new_proto,encl_func_func_def):
    def create_new_proto(module_name,str_node,proto_obj):
        #obj_id = get_meta_obj_id(module_name+":"+str_node)
        obj_id = get_meta_obj_id(str_node)
        #print("MMMMM ", obj_id, module_name+"   "+str_node)
        if obj_id not in objects:
            obj = datatypes.Object("proto",module_name=module_name,prototype=proto_obj)
            #obj.pretty_print()
            objects[obj_id] = obj
        return obj_id
    if is_universal_constant(new_proto):
        #print("new proto: Constant before encoding: ",str(new_proto),type(new_proto))
        c_str = encode_constant(new_proto)
        #print("Encoded constant",c_str)
        change = pt_graph.addEdge(lhs,c_str,"")
    else:
        proto_obj_id = create_new_proto(module_name,str(new_proto),cast_proto_container(new_proto))
        change = pt_graph.addEdge(lhs,proto_obj_id,"")
        #print("Here in new field read proto: ", str(new_proto), change)
        if "_class_initializer" in encl_func_func_def.name or "_module_initializer" in encl_func_func_def.name :
            ... # maybe we do nothing here
            #ff = encl_func_func_def.name
        else:
            ff = encl_path[encl_func_func_def]
            if proto_obj_id not in obj_id_to_encl:
                obj_id_to_encl[proto_obj_id] = [ff]
            else:
                #print(proto_obj_id)
                #print(ff)
                #print(obj_id_to_encl[proto_obj_id])
                #assert obj_id_to_encl[proto_obj_id] == ff
                ll = obj_id_to_encl[proto_obj_id]
                if ff not in ll: ll.append(ff)
                obj_id_to_encl[proto_obj_id] = ll
    return change    

def check_k_limit(lhs):
    k_limit = 2
    count = 0
    for obj_Edge in pt_graph.getEdgesFromSource(lhs):
        obj_id = obj_Edge.tgt
        if is_constant(obj_id) or objects[obj_id].kind == 'proto':
            count = count+1
    if count >= k_limit:
        return True
    else:
        return False

# ====== PT Graph Addition =======

# Processes x = y pt basic statement
# Requires x is var_id, y is var_id or c_constant
def x_eq_y(x,y):
    change = False
    if is_constant(y):
        change = pt_graph.addEdge(x,y,"")
    else:
        for obj_Edge in pt_graph.getEdgesFromSource(y):
            obj_id = obj_Edge.tgt
            change = pt_graph.addEdge(x,obj_id,"") or change
    return change

# Processes x.f = y (or x[f] = y) 
# Requires x is var_id, y is var_id or c_constant
def x_f_eq_y(x,f,y):
    change = False
    if is_constant(x): return change
    #print(len(pt_graph.getEdgesFromSource(x)), len(pt_graph.getEdgesFromSource(y)))
    for obj1_Edge in pt_graph.getEdgesFromSource(x):
        obj1_id = obj1_Edge.tgt
        if is_constant(obj1_id): continue
        obj1 = objects[obj1_id]
        if obj1.kind != 'user': continue
        #obj1.pretty_print()
        if is_constant(y):
            change = pt_graph.addEdge(obj1_id,y,f) or change
        else:
            for obj2_Edge in pt_graph.getEdgesFromSource(y):
                obj2_id = obj2_Edge.tgt
                change = pt_graph.addEdge(obj1_id,obj2_id,f) or change
    return change

# Requires x and y are both var_id's
def x_eq_y_f(x,y,f):
    change = False
    for obj1_Edge in pt_graph.getEdgesFromSource(y):
        obj1_id = obj1_Edge.tgt
        for obj2_Edge in pt_graph.getEdgesFromSource(obj1_id):
            obj2_id = obj2_Edge.tgt
            if obj2_Edge.label != f: continue
            change = pt_graph.addEdge(x,obj2_id,"") or change
    return change


# === Filtering of args at a proto call

# Takes a list of arguments and filters out "user-defined". Leaves constants
def filter(arg_arr):
    proto_arg_lists = []
    for arg_i in arg_arr:
        arg_i_list = []
        if is_constant(arg_i): 
            arg_i_list.append(decode_constant(arg_i))
        elif ins(arg_i,list):
            for v in arg_i:
                #print("v ",v)
                if is_constant(v):
                   arg_i_list.append(decode_constant(v))
                   continue 
                for obj_edge in pt_graph.getEdgesFromSource(v):
                    obj_id = obj_edge.tgt
                    #print("--- obj_id",obj_id)
                    if obj_id in objects:
                        obj = objects[obj_id]
                        #print("Here in obj_id...")
                        #obj.pretty_print()
                        if obj.kind == "proto":
                            # arg_i_list.append(obj)
                            arg_i_list.append(obj.prototype)
                    elif is_constant(obj_id):
                        arg_i_list.append(decode_constant(obj_id))                 
        if arg_i_list == []: 
            return None # We have no concrete set of args to evaluate
        else:
            proto_arg_lists.append(arg_i_list)
    return proto_arg_lists        
        
def cart_prod(arg_list):
    result = []
    if len(arg_list) == 0:
        return [[]]
    elif len(arg_list) == 1:
        for arg_i in arg_list[0]:
            result.append([arg_i])
    else:
        partial = cart_prod(arg_list[1:])
        for arg_i in arg_list[0]:
            for arg_list in partial:
                result.append([arg_i] + arg_list)
    return result                
    
# ==== Analysis result    

# FunctionDef -> List(Stmt)
# Invariant: stmts.keys == Reachable methods
stmts = {}
# FunctionDef -> {} local environment map from locals to var ids. Parallel
local_env = {}
# FunctionDef or ClassDef -> str module_name
module_names = {}
# FunctionDef -> str enclosed func/class path
encl_path = {}

# FunctionDef -> ClassDef
# The enclosing class of the FunctionDef
encl_class = {} 

# Module initializers
# FunctionDefs elements
entry_points = []

# Threashold builtin module 
# Module
typeshed_builtins_module = None

# A map from ClassDef to "fake" class_initializer method
class_initializers = {}

def add_stmt(func_def,stmt):
    # TODO: Add a constraint only if not already there
    if func_def not in stmts:
        stmts[func_def] = []
    stmts[func_def].append(stmt)
        
# ==== Class hierarchy

superclasses = {}
mros = {}
properties = {}

# ==== End class hierarchy code


def print_globals():
    # global vars, meta_objects, objects
    '''
    print("Variable name to var id mapping:")
    for var_name in vars:
        print(var_name," -> ",vars[var_name])
    print("Variable name to meta object id mapping:")
    for var_name in meta_objects:
        print(var_name," -> ",meta_objects[var_name])
        objects[meta_objects[var_name]].pretty_print()        
    print("Object var to object mapping:")
    for obj_id in objects:
        print(obj_id," -> ")
        objects[obj_id].pretty_print()

    print("Stmts:")
    for func_def in stmts:
        print("-----",func_def, func_def.name,"-----")
        for stmt in stmts[func_def]:
            stmt.pretty_print()
        print("----- end of",func_def.name,"-----")
    '''
    print('\n ------ Printing var pt sets ------ \n')
    num_vars = 0
    pt_set_size = 0
    all_vars = 0
    for func_def in stmts:
        print("\nAnd the function is ", func_def.name, "in",module_names[func_def])
        for v in local_env[func_def]:
            var_id = local_env[func_def][v]
            all_vars += 1
            print("> ", v,'maps to',var_id)
            empty = True
            for obj_Edge in pt_graph.getEdgesFromSource(var_id):
                print("...")
                empty = False
                obj_id = obj_Edge.tgt
                if obj_id.startswith('c_'):
                    print("Constant: ", obj_id)
                else:
                    obj = objects[obj_id]
                    obj.pretty_print()
                    if v == "rules_with_whitespace":
                        for obj2_Edge in pt_graph.getEdgesFromSource(obj_id):
                            print("-- And field: ",obj_id,'.',obj2_Edge.label," is ", obj2_Edge.tgt)
                            if obj2_Edge.tgt in objects:
                                objects[obj2_Edge.tgt].pretty_print()
                            
                pt_set_size += 1
            if empty == False: 
                num_vars += 1
            else:
                print("EMPTY")
    print("Size of objects map, stmts map: ", len(objects), len(stmts))  
    print("Avg size of non-empty pt set: ",float(pt_set_size/num_vars)) if num_vars > 0 else print("!!! num_vars = 0 !!! danger?")
    print("All vars vs non-empty vars:",all_vars,num_vars, "("+str(round((all_vars-num_vars)/all_vars,2)*100)+"%)")          

def short_path(x):
    if x is None: return None
    cpd = curr_package_dir[:-1]
    #print(cpd)
    x = x.replace(cpd,"")
    #a = "/.../pt_analysis"
    #b = "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages"
    #c = "/.../DLInfer_data/DLInfer_data/orig_pro_dynamic/cerberus"

    #ll = ["/.../DLInfer_data/DLInfer_data/orig_pro_dynamic/cerberus",
    #"/.../DLInfer_data/DLInfer_data/orig_pro_dynamic/sc2",
    #"/.../DLInfer_data/DLInfer_data/orig_pro_dynamic/pygal",
    #"/.../DLInfer_data/DLInfer_data/orig_pro_dynamic/mtgjson",
    #"/.../DLInfer_data/DLInfer_data/orig_pro_dynamic/zfsp",
    #]
    #xx = x.replace(a,"").replace(b,"").replace(c,"")
    #for l in ll:
    #    xx = xx.replace(l,"")
    #return xx
    return x

def get_obj_name(obj):
    s = ""
    if obj.kind == "meta_cls":
        s += "meta_cls|{}|{}".format(short_path(obj.module_name), short_path(obj.cls.name))
    elif obj.kind == "meta_func":
        s += "({})meta_func|{}|{}".format(short_path(obj.func.name), short_path(obj.module_name), obj.closure_bindings)
    elif obj.kind == "user":
        t = "user|{}|{}".format(short_path(obj.module_name), get_obj_name(obj.cls_meta_obj))
        tt = t.split("|")
        #print(tt)
        s += "({})".format(tt[-1])
        for i in range(0,len(tt)-1):
            s += tt[i]
            if i < len(tt)-2:
                s += "|"
    elif obj.kind == "proto":
        s += "proto|{}".format(obj.prototype)
    elif obj.kind == "tuple_builtin" or obj.kind == "list_builtin" or obj.kind == "dict_builtin":
        s += "({}){}".format(obj.kind, short_path(obj.module_name))
    else:
        s += "Unknonwn object:{}".format(self.kind)
    return s

# var_id -> [file_path, func_name, line no, col offset]
varid_to_lineno = {}
inferred_types_lineno = {}

# name of the entry function
main_name = "main"
# debug note to be printed at the end of the run
global_note = ""
# dict of inferred types. Key = (file name, func name, var). Value = List of inferred types
inferred_types = {}
write_pkl_name = ""
write_pkl_base = ""

def de_dupe(l):
    ll = []
    for i in l:
        if i not in ll:
            ll.append(i)
    return ll

def is_int(x):
    a = x.replace("c_","")
    try:
        int(a)
        return True
    except ValueError:
        return False

def is_float(x):
    a = x.replace("c_","")
    try:
        float(a)
        return True
    except ValueError:
        return False

def process_types(printing = False):
    if printing: print("\n\nProcessing types")
    for func_def in stmts:
        if printing: print("\nFUNCTION =", func_def.name, "in",short_path(module_names[func_def]))
        for v in local_env[func_def]:
            var_id = local_env[func_def][v]
            if printing: 
                print("> var (var_id):", "{} ({})".format(v, var_id))
                print("{} ({})".format(v,var_id))
            empty = True
            type_list = []
            literal_list = []
            for obj_Edge in pt_graph.getEdgesFromSource(var_id):
                #print("...")
                empty = False
                obj_id = obj_Edge.tgt
                if obj_id.startswith('c_'):
                    #print("Constant: ", obj_id)
                    literal_list.append(obj_id)
                    if obj_id == "c_False" or obj_id == "c_True":
                        c_type = "bool"
                    elif obj_id == "c_None":
                        c_type = "None"
                    elif is_int(obj_id):
                        c_type = "int"
                    elif is_float(obj_id):
                        c_type = "float"
                    elif obj_id == "c_'msg'":
                        c_type = "string"
                    else:
                        c_type = "string" + "("+obj_id+")"
                    type_list.append(c_type)
                    #type_list.append(obj_id.replace("c_",""))
                else:
                    obj = objects[obj_id]
                    #obj.pretty_print()
                    ss = get_obj_name(obj)
                    literal_list.append(ss)
                    type_list.append(ss)
            #print("  ", literal_list)
            #print("  ", type_list)
            key = (short_path(module_names[func_def]), func_def.name, v)
            inferred_types[key] = de_dupe(type_list)

            if var_id in varid_to_lineno:
                ll = varid_to_lineno[var_id]
            else:
                ll = []
            inferred_types_lineno[key] = ll

    if 1:
        inferred_dict_to_pkl("")

def inferred_dict_to_pkl(p):
    #base = "/.../pt_analysis/inferred_types/cerberus/"
    #path = base + "test.pkl"

    path = write_pkl_base + write_pkl_name
    #print(path)
    #assert False

    if 1:
        if not os.path.exists(write_pkl_base):
            os.makedirs(write_pkl_base)
        with open(path, 'wb') as f:
            pickle.dump(inferred_types, f, protocol=pickle.HIGHEST_PROTOCOL)

def cg_nodes_to_pkl():
    #base = "/.../pt_analysis/inferred_types/cerberus/cg_nodes/"
    base = write_pkl_base + "/cg_nodes/"
    path = base + write_pkl_name
    
    if 0:
        with open(path, 'wb') as f:
            pickle.dump(call_graph.nodes, f, protocol=pickle.HIGHEST_PROTOCOL)   
    #print("\n\n\n>>> ", call_graph.nodes) 
    call_graph.printGraph(encl_class)


dd_global = {}
varid_to_name = {}

def init_varid_to_name(): # unused for now
    for f_def in stmts:
        for v in local_env[f_def]:
            var_id = local_env[f_def][v]
            #print("> var (var_id):", "{} ({})".format(v, var_id))
            #rint("{} ({})".format(v,var_id))
            if var_id not in varid_to_name:
                varid_to_name[var_id] = v
            else:
                vv = varid_to_name[var_id]
                assert v == vv
    #print(len(varid_to_name))
    #assert False
def rpl(x):
    if x is None: return None
    #pp = ["/.../pt_analysis/orig_pro_dynamic/cerberus/",
    #    "/.../pt_analysis/orig_pro_dynamic/pygal/",
    #    "/.../pt_analysis/orig_pro_dynamic/mtgjson/",
    #    "/.../pt_analysis/orig_pro_dynamic/sc2/",
    #    "/.../pt_analysis/orig_pro_dynamic/zfsp/",
    #    "/.../pt_analysis/orig_pro_dynamic/invoke/"]
    #for p in pp:
    #    x = x.replace(p,"")
    x = x.replace(curr_package_dir, "")
    return x
def get_obj_name_v2(obj):
    #print("Original =", get_obj_name(obj))
    s = ""
    if obj.kind == "meta_cls":
        #s += "meta_cls|{}|{}".format(short_path(obj.module_name), short_path(obj.cls.name))
        s += "meta_cls,{},{}".format(rpl(obj.module_name), short_path(obj.cls.name))
        return s
        # what do we do ???
    elif obj.kind == "meta_func":
        #s += "({})meta_func|{}|{}".format(short_path(obj.func.name), short_path(obj.module_name), obj.closure_bindings)
        nice_path_format = rpl(encl_path[obj.func])
        #print("xx =", nice_path_format)
        return nice_path_format
    elif obj.kind == "user":
        t = "user|{}|{}".format(rpl(obj.module_name), get_obj_name(obj.cls_meta_obj))
        tt = t.split("|")
        #print(tt)
        s += "({})".format(tt[-1])
        for i in range(0,len(tt)-1):
            s += tt[i]
            if i < len(tt)-2:
                s += "|"
        return s
    elif obj.kind == "proto":
        s += "proto,{}".format(obj.prototype)
        return s
    elif obj.kind == "tuple_builtin" or obj.kind == "list_builtin" or obj.kind == "dict_builtin":
        #s += "({}){}".format(obj.kind, short_path(obj.module_name))
        s += "{},{}".format(obj.kind, rpl(obj.module_name))
    else:
        s += "Unknonwn object:{}".format(self.kind)
        assert False
    return s

def find_func_of_oid(o_id):
    assert False
    for f_def in local_env:
        print(f_def, f_def.name)
        #print(local_env[f_def])
        for v_name in local_env[f_def]:
            v_id = local_env[f_def][v_name]
            print("  ", v_name, v_id)
            for obj_Edge in pt_graph.getEdgesFromSource(v_id):
                obj_id = obj_Edge.tgt
                print("    obj_id =", obj_id)

def get_more_callgraph_info_from_ptgraph(printing = False):
    #print("\n~~~")
    #init_varid_to_name()
    #for func_def in stmts:
    #    print("\nFUNCTION =", func_def.name, "in",short_path(module_names[func_def]))

    list_of_funcdef = []
    dd = {}
    for key in call_graph.edges.keys():
        for edge in call_graph.edges[key]:
            assert isinstance(edge.src, ast.FunctionDef) or isinstance(edge.src, ast.AsyncFunctionDef)
            assert isinstance(edge.tgt, ast.FunctionDef) or isinstance(edge.tgt, ast.AsyncFunctionDef)
            extra_src = " (in "+encl_class[edge.src].name+")" if encl_class != None and edge.src in encl_class else ""
            extra_tgt = " (in "+encl_class[edge.tgt].name+")" if encl_class != None and edge.tgt in encl_class else ""
            if printing: print("Call from ",edge.src.name+extra_src," to ",edge.tgt.name+extra_tgt) 
            
            #print(type(edge.src), edge.src.name)
            #print(type(edge.tgt), edge.tgt.name)
            #assert edge.src in stmts and edge.tgt in stmts
            if edge.src not in list_of_funcdef:
                list_of_funcdef.append(edge.src)
            if edge.tgt not in list_of_funcdef:
                list_of_funcdef.append(edge.tgt)
            xx = ""
            yy = ""
            ep = encl_path
            if edge.src in ep: xx = rpl(ep[edge.src])
            else: assert False
            if edge.tgt in ep: yy = rpl(ep[edge.tgt])
            else: assert False
            if printing: print("    >> ",xx," to ",yy)
            if xx not in dd:
                dd[xx] = [yy]
            else:
                ll = dd[xx]
                ll.append(yy)
                dd[xx] = ll
    
    #print("")
    def find_name(func_def, var_id):
        #if var_id in varid_to_name:
        #    print("var_id =", var_id, " varid_to_name =", varid_to_name[var_id])
        #    return varid_to_name[var_id]
        return "NoName"

    #print("?????")
    for func_def in list_of_funcdef:
        #if func_def.name == "__normalize_coerce":
        #print("\nHere at ", func_def.name)
        if True:
            #print(stmts[func_def])
            f_name = rpl(encl_path[func_def])
            #print("\n",f_name)
            ll = []
            if func_def not in stmts: continue
            for s in stmts[func_def]:
                #print(type(s))
                #print("")
                #print(s.pretty_print())
                if isinstance(s, CallStmt):
                    #print(s.pretty_print())
                    #print(type(s.funcs))
                    if len(s.funcs) == 0: continue
                    first_elem = s.funcs[0]
                    #str_name = find_name(func_def, first_elem)

                    #print("First element =", first_elem, "name =", str_name)
                    gEFS = pt_graph.getEdgesFromSource(first_elem)
                    #print("First element =", first_elem, "   len() =", len(gEFS))
                    if len(gEFS) != 0:
                        for obj_Edge in gEFS:
                            obj_id = obj_Edge.tgt
                            if obj_id.startswith('c_'):
                                ... # Do nothing
                                #print("Constant: ", obj_id)
                                #assert False
                            else:
                                obj = objects[obj_id]
                                #obj.pretty_print()
                                ss = get_obj_name_v2(obj)
                                #print("ss =", ss,"\n")
                                if ss not in ll: 
                                    ll.append(ss)
                        ...
                    else:
                        ... # TBD (or not???)        


                    #for l in s.funcs:
                    #    print(">",type(l))
                    #    print(l)
                    # print("")
            if f_name not in dd:
                dd[f_name] = ll
            else:
                l2 = dd[f_name]
                for l in ll:
                    if l not in l2:
                        l2.append(l)
                dd[f_name] = l2
            #print("---")

    # check list/dict/tuple objects in meta_objects
    for m in meta_objects:
        o_id = meta_objects[m]
        oo = objects[o_id]
        ll = ["tuple_builtin", "list_builtin", "dict_builtin"]
        #if "_expand_composed_of_rules" in m:
        if True:
            assert isinstance(oo, datatypes.Object)
            #print("> ", m, o_id)
            ###print("   ", type(oo), oo)
            #print("   ", oo.kind)
            if o_id in obj_id_to_encl:
                ll = obj_id_to_encl[o_id]
                for l in ll:
                    l1 = rpl(l)
                    #print("   ", l1, "\n")
                    if "<class 'tuple'>" in m:
                        ee = "<builtin>.tuple"
                        if l1 in dd:
                            a = dd[l1]
                            if ee not in a: a.append(ee)
                            dd[l1] = a
                        else:
                            dd[l1] = [ee]
                    elif "<class 'list'>" in m:
                        ee = "<builtin>.list"
                        if l1 in dd:
                            a = dd[l1]
                            if ee not in a: a.append(ee)
                            dd[l1] = a
                        else:
                            dd[l1] = [ee]
                    elif "<class 'dict'>" in m:
                        ee = "<builtin>.dict"
                        if l1 in dd:
                            a = dd[l1]
                            if ee not in a: a.append(ee)
                            dd[l1] = a
                        else:
                            dd[l1] = [ee]
            #if oo.kind in ll:
            #    print("**********", oo.kind,"\n")
            #    assert False
            #elif oo.kind == "proto":
            #    print(oo.prototype)
            #elif m == "<class 'tuple'>":
            #    ...
                #find_func_of_oid(o_id)
                #print(type(oo.prototype), oo.prototype, "\n")
                #assert False

    #print(dd_global)
    if False:
        for d in dd:
            print(d)
            aa = dd[d]
            for a in aa:
                print("  ", a)

    base = write_pkl_base + "cg_nodes_v2/"
    path = base + write_pkl_name
    if 1:
        if not os.path.exists(base):
            os.makedirs(base)
        with open(path, 'wb') as f:
            pickle.dump(dd, f, protocol=pickle.HIGHEST_PROTOCOL)   


    #print("~~~ \n")
package_name = ""
curr_package_dir = ""

# for running unit tests. Is there a better way to handle this?
def reset_globals():
    global pt_graph
    global call_graph
    global mirror_call_graph
    global var_to_encl_func
    global fresh_id
    global obj_id
    global vars
    global meta_objects
    global objects
    global package_env
    global stmts
    global local_env
    global superclasses
    global mros
    global encl_path
    global encl_class
    global module_names
    global entry_points
    global class_initializers
    global properties

    global inferred_types
    global main_name
    global write_pkl_name
    global write_pkl_base
    global varid_to_lineno
    global inferred_types_lineno
    global dd_global
    global varid_to_name
    global package_name
    global obj_id_to_encl
    global curr_package_dir

    pt_graph = Graph()
    call_graph = Graph()
    mirror_call_graph = Graph()
    var_to_encl_func = {}
    fresh_id = 0
    obj_id = 0
    vars = {}
    meta_objects = {}
    objects = {}
    package_env = {}
    stmts = {}
    local_env = {}
    module_names = {}
    superclasses = {}
    mros = {}
    encl_path = {}
    entry_points = []
    class_initializers = {}
    encl_class = {}
    properties = {}

    main_name = "main"
    global_note = ""
    inferred_types = {}
    write_pkl_name = ""
    write_pkl_base = ""
    varid_to_lineno = {}
    inferred_types_lineno = {}
    dd_global = {}
    varid_to_name = {}
    package_name = ""
    obj_id_to_encl = {}
    curr_package_dir = ""