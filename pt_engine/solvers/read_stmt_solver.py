import ast

import pt_engine.globals as globals
import pt_engine.datatypes as datatypes
import pt_engine.visitors.function_visitor as function_visitor

from ..solvers.stmt import Stmt, find_property
from ..utils.base import ins, is_constant, is_universal_constant, encode_constant
from ..solvers.call_stmt_solver import _processCall

class ReadStmt(Stmt):
    def __init__(
             self,
             kind,
             encl_func,
             lhs,
             rhs,
             fld,
             is_super=False
    ):
        super().__init__(kind,encl_func,lhs)
        self.rhs = rhs
        self.fld = fld
        self.is_super = is_super
    def pretty_print(self):
        print("Read",self.lhs,"=",self.rhs,".",self.fld)
    def solve(self):
        #print("\n=== AT read_stmt_solver.solve() ===", self.encl_func)
        #self.pretty_print()
        change = False
        for obj_edge in globals.pt_graph.getEdgesFromSource(self.rhs):
            obj_id = obj_edge.tgt # Get receiver object
            if is_constant(obj_id): continue # This was a constant object, imprecision
            obj = globals.objects[obj_id]
            #print(">> ")
            #obj.pretty_print()
            if not (obj.kind == 'proto' or obj.kind == 'user' or obj.kind == 'dict_builtin'): continue 
            if obj.kind == 'proto':
                try:
                    # No need to import env. Since we have gotten the proto object, that means env is on
                    new_proto = getattr(obj.prototype,self.fld)
                    # print("We got the proto", str(obj.prototype),self.fld)
                except:
                    # print("Didn't get the proto: ", str(obj.prototype),self.fld)
                    continue    
                if globals.check_k_limit(self.lhs): continue
                # print("A new field proto: ", obj.prototype, self.fld)
                change = globals.new_proto(obj.module_name,self.lhs,new_proto,self.encl_func) or change
            ### special case of biult-in functions BEGIN ###
            elif obj.kind == 'dict_builtin':
                # TODO: Need to implement search through typeshed
                #pass
                # print("Passing here... keys",self.fld)
                # obj.pretty_print()
                '''
                obj.pretty_print()
                if self.fld == "keys": 
                    keys_list = None
                    for obj_edge2 in globals.pt_graph.getEdgesFromSource(obj_id):
                        print("And the label is:",obj_edge2.label)
                        if obj_edge2.label == "keys_list":
                            keys_list = obj_edge2.tgt
                    assert keys_list != None
                    key_index = 0
                    for obj_edge2 in globals.pt_graph.getEdgesFromSource(obj_id):
                        if obj_edge2.label == "keys_list" or obj_edge2.label == '*': continue
                        if is_universal_constant(obj_edge2.label): # TODO: skipping proto constants for now
                            change = globals.pt_graph.addEdge(keys_list,encode_constant(obj_edge2.label),key_index) or change
                        key_index += 1
                    change = globals.pt_graph.addEdge(self.lhs,keys_list,"")       
                '''    
            elif obj.kind == 'user' and self.fld == "__class__":
                meta_obj_id = globals.meta_objects[obj.cls_meta_obj.module_name+":"+obj.cls_meta_obj.cls.name]
                change = globals.pt_graph.addEdge(self.lhs,meta_obj_id,"") or change               
            ### special case of biult-in functions END ###    
            elif obj.kind == 'user':
                #print("== At user ==")
                # Now check for getters: 
                getter_def = find_property(obj.cls_meta_obj.cls,self.fld,'getter')
                if getter_def != None:
                    globals.module_names[getter_def] = obj.cls_meta_obj.module_name
                    change = _processCall([obj_id],[],getter_def,self.lhs,self.encl_func) or change 
                    globals.encl_class[getter_def] = obj.cls_meta_obj.cls # For pretty printing 
                # Now look for pt field edges
                for fld_edge in globals.pt_graph.getEdgesFromSource(obj_id):
                    #print("fld_edge.label =", fld_edge.label)
                    if self.fld == fld_edge.label:
                        change = globals.pt_graph.addEdge(self.lhs,fld_edge.tgt,"") or change
                        if is_constant(fld_edge.tgt): continue
                        tgt_obj = globals.objects[fld_edge.tgt]                          
                        # If closure with obj_id receiver already in, we continue
                        if tgt_obj.kind == 'meta_func' and tgt_obj.closure_bindings != None and tgt_obj.closure_bindings == obj_id:
                            continue 
                # Now look for functions and create the closure function def object
                # TODO: Revisit super!
                mros = globals.mros[globals.encl_class[self.encl_func]][1:] if self.is_super==True else globals.mros[obj.cls_meta_obj.cls]
                found = False
                #print("self.fld =", self.fld)
                for cls in mros:
                    for elem in cls.body:
                        #if ins(elem, ast.FunctionDef):
                        #    print("elem =", elem.name)
                        if (ins(elem,ast.FunctionDef) or ins(elem,ast.AsyncFunctionDef)) and elem.name == self.fld:
                            #print("HEREE")
                            encl_module_name = globals.module_names[cls]
                            full_var_name = encl_module_name+":"+cls.name+":"+obj_id+":"+self.fld # Creating the closure object for the function
                            var_id = globals.get_var_id(full_var_name)
                            meta_obj_id = globals.get_meta_obj_id(full_var_name)
                            if meta_obj_id not in globals.objects:
                                #print("INNN", meta_obj_id)
                                #assert False
                                globals.objects[meta_obj_id] = datatypes.Object("meta_func",func=elem,module_name=encl_module_name,closure_bindings=[obj_id])
                                globals.encl_class[elem]=cls # Just for pretty printing of call graph.
                            else:
                                #print("ELSEE")
                                ...
                            change = globals.pt_graph.addEdge(self.lhs,meta_obj_id,"") or change 
                            found = True    
                            break 
                    if found: break    
                # And now we'll look for "fields" in class initializers
                current_cls = obj.cls_meta_obj.cls
                if current_cls in globals.class_initializers:
                    class_init = globals.class_initializers[obj.cls_meta_obj.cls]
                    init_local_env = globals.local_env[class_init]
                    if self.fld in init_local_env:
                        var_id = init_local_env[self.fld]
                        # print("Found a class field!", self.fld)
                        globals.x_eq_y(self.lhs,var_id)
                        
                          
        result = [self.encl_func] if change else []
        return result

