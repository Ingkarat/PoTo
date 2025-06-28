#import ast

import pt_engine.globals as globals

from ..solvers.call_stmt_solver import _processCall
from ..utils.base import ins, is_constant, decode_constant, is_proto_container
from ..solvers.stmt import Stmt, find_property

class UpdateStmt(Stmt):
    def __init__(
             self,
             kind,
             encl_func,
             lhs,
             rhs,
             fld,
    ):
        super().__init__(kind,encl_func,lhs)
        self.rhs = rhs
        self.fld = fld
        self.hash = 0
    def pretty_print(self):
        print("Update:",self.lhs,".",self.fld,"=",self.rhs, " in function ", self.encl_func.name)
    def hash_fun(self):
        result = len(globals.pt_graph.getEdgesFromSource(self.lhs))
        result += 1 if is_constant(self.rhs) else len(globals.pt_graph.getEdgesFromSource(self.rhs))
        return result
    def solve(self):
        result = []
        modified_objs = []
        # TODO: THIS NEEDS A FIX. This is a case for obj. sens analysis.
        if "among.py" in globals.module_names[self.encl_func]: return result
        if self.hash_fun() == self.hash: return []
        #print("Just starts solve ",self.lhs,".",self.fld,"=",self.rhs)
        change = globals.x_f_eq_y(self.lhs,self.fld,self.rhs)
        #print("And after x_f_eq_y in pt...")
        # self.pretty_print()
        # The following code ads handling of properties
        local_change = False
        for obj_edge in globals.pt_graph.getEdgesFromSource(self.lhs):
            obj_id = obj_edge.tgt
            if change: modified_objs.append(obj_id) #If there was a change, we add to potentially modified; can be optimized.
            if is_constant(obj_id): continue
            obj = globals.objects[obj_id]
            if obj.kind != 'user': continue
            cls_obj = obj.cls_meta_obj.cls
            #print("HERE 1, before find property ")
            setter_def = find_property(cls_obj,self.fld,'setter')
            #print("HERE 2, after find property ")
            if setter_def == None: continue
            #print("HERE, setter_def",setter_def.name,obj.cls_meta_obj.module_name, self.rhs)
            globals.module_names[setter_def] = obj.cls_meta_obj.module_name
            globals.encl_class[setter_def] = obj.cls_meta_obj.cls # For pretty printing call graph
            local_change = _processCall([obj_id]+[[self.rhs]],[],setter_def,None,self.encl_func) or local_change 
            if local_change and obj_id not in modified_objs: modified_objs.append(obj_id)
        change = local_change or change           
        # Add all reachable methods back to worklist    
        if change: 
            _find_target_functions(modified_objs,result)
            #for f in globals.stmts:
            #    if f.name == "module_initializer": continue #ANA: REVISIT!
            #    if f not in result: result.append(f)        
            self.hash = self.hash_fun()        
        return result

class AssignStmt(Stmt):
    def __init__(
             self,
             kind,
             encl_func,
             lhs,
             rhs
    ):
        super().__init__(kind,encl_func,lhs)
        self.rhs = rhs
        self.hash = 0
    def pretty_print(self):
        print("Assign",self.lhs,"=",self.rhs)
    def hash_fun(self):
        result = 1 if is_constant(self.rhs) else len(globals.pt_graph.getEdgesFromSource(self.rhs))
        return result    
    def solve(self):
        # self.pretty_print()
        if self.hash == self.hash_fun(): return []
        change = False
        result = []
        change = globals.x_eq_y(self.lhs,self.rhs)
        # if change == False: return []
        if change == True: result = [self.encl_func]
        # Need to add callers to worklist if lhs is ret_var
        is_ret_var = False
        for var in globals.local_env[self.encl_func]:
            if var == self.encl_func.name+"_ret":
                if globals.local_env[self.encl_func][var] == self.lhs:
                    is_ret_var = True
        if is_ret_var: 
            for callerEdge in globals.call_graph.getEdgesToTarget(self.encl_func):
                caller = callerEdge.src
                # print("TYPE OF LABEL", type(callerEdge.label),callerEdge.label)
                new_change = False
                for caller_lhs in callerEdge.label:
                    new_change = globals.x_eq_y(caller_lhs,self.lhs) or new_change
                # TODO: Check this out for correctness.
                if new_change and (caller not in result): 
                    result.append(caller)
        if result != []: 
            self.hash = self.hash_fun()            
        return result
    
class BinOpStmt(Stmt):
    def __init__(
             self,
             kind,
             encl_func,
             lhs,
             left,
             right,
             binop
    ):
        super().__init__(kind,encl_func,lhs)
        self.left = left
        self.right = right
        self.binop = binop
        self.hash = 0
    def pretty_print(self):
        print("BinOp in",self.encl_func.name,self.lhs,"=",self.left,self.binop,self.right)
    def hash_fun(self):
        result = 1 if is_constant(self.left) else len(globals.pt_graph.getEdgesFromSource(self.left))
        result += 1 if is_constant(self.right) else len(globals.pt_graph.getEdgesFromSource(self.right))
        return result    
    def solve(self):
        # self.pretty_print()
        if self.hash == self.hash_fun(): return []
        change = False
        left = self.left if is_constant(self.left) else [self.left]
        right = self.right if is_constant(self.right) else [self.right]
        left_right = [left,right]
        #print("bin_op arg_list: ",left_right)
        filtered = globals.filter(left_right)
        #print("bin_op filtered: ",filtered)
        found_new_proto = False
        if filtered != None:
            filtered = globals.cart_prod(filtered)
            for arg_list in filtered:
                exec_str = ""
                assert len(arg_list)==2
                exec_str = exec_str+arg_list[0] if ins(arg_list[0],str) else exec_str + 'arg_list['+str(0)+']'
                exec_str = exec_str + self.binop
                exec_str = exec_str+arg_list[1] if ins(arg_list[1],str) else exec_str + 'arg_list['+str(1)+']'
                exec_str = 'new_proto = '+exec_str
                if globals.check_k_limit(self.lhs): continue
                try:
                    locals = {'arg_list':arg_list}
                    #print("Executing in BinOp",self.encl_func.name,exec_str)
                    exec(exec_str,None,locals)
                except:
                    #print("Threw an exception in BinOp...", exec_str)
                    #self.pretty_print()
                    pass
                # TODO: Add here!
                if 'new_proto' in locals:    
                    if globals.check_k_limit(self.lhs): continue
                    new_proto = locals['new_proto']
                    # print("Here, and the result is ", new_proto)
                    change = globals.new_proto(globals.module_names[self.encl_func],self.lhs,new_proto,self.encl_func) or change  
                    found_new_proto = True
        if found_new_proto == False:     
            # If there is no concrete solution for op, try abstract solution       
            # print("bin_op left_right",left_right)
            for next_arg in left_right:
                # print("next_arg ",next_arg)
                if is_constant(next_arg):
                    change = globals.pt_graph.addEdge(self.lhs,next_arg,'') or change
                else:
                    for var in next_arg:
                        for objEdge in globals.pt_graph.getEdgesFromSource(var):
                            if is_constant(objEdge.tgt) or globals.objects[objEdge.tgt].kind not in ('user','meta_func','meta_cls'):
                                change = globals.pt_graph.addEdge(self.lhs,objEdge.tgt,'') or change          

        ret_set = [self.encl_func] if change else []
        if ret_set != []:
            self.hash = self.hash_fun()
        return ret_set

class SubscriptUpdateStmt(Stmt):
    def __init__(
             self,
             kind,
             encl_func,
             lhs,
             index,
             rhs
    ):
        super().__init__(kind,encl_func,lhs)
        self.index = index
        self.rhs = rhs
    def pretty_print(self): 
        print("SubscriptUpdate in ",self.encl_func.name,self.lhs,"["+str(self.index)+']=',self.rhs)
    def solve(self):
        # self.pretty_print()
        change = False
        result = []
        modified_objs = []
        for obj_Edge in globals.pt_graph.getEdgesFromSource(self.lhs):
            obj_id = obj_Edge.tgt
            if is_constant(obj_id): continue 
            obj = globals.objects[obj_id]
            if not (obj.kind == 'tuple_builtin' or obj.kind == 'list_builtin' or obj.kind == 'dict_builtin' or is_proto_container(obj)): continue
            the_index = _refine_index(self.index)
            #print("the index",self.index)
            if is_constant(self.rhs):
                local_change = globals.pt_graph.addEdge(obj_id,self.rhs,the_index) 
                #print("Adding edge ", obj_id,"[",self.index,"]",self.rhs)
            else:   
                local_change = False 
                for obj2_Edge in globals.pt_graph.getEdgesFromSource(self.rhs):
                    obj2_id = obj2_Edge.tgt
                    #print("Adding edge ", obj_id,obj2_id)
                    local_change = globals.pt_graph.addEdge(obj_id,obj2_id,the_index) or local_change
            change = local_change or change
            if local_change: modified_objs.append(obj_id)        
        if change: 
            _find_target_functions(modified_objs,result)
            #for f in globals.stmts:
            #    if f.name == "module_initializer": continue #ANA: REVISIT!
            #    if f not in result: result.append(f)  
        return result

def _refine_index(index):
    if not ins(index,list): return index # It is a decoded constant 
    if len(index) == 1:
        if is_constant(index[0]):
            return decode_constant(index[0])
        else:
            if len(globals.pt_graph.getEdgesFromSource(index[0])) == 1:
                for obj_Edge in globals.pt_graph.getEdgesFromSource(index[0]):
                    if is_constant(obj_Edge.tgt):
                        return decode_constant(obj_Edge.tgt)
    return '*' # Cannot refine, worst case

# Takes a list of modified objects and computes the list of all function defs in result
# for which there is a variable that points to a modified object and therefre may be affected by the change
def _find_target_functions(modified_objs,result):
    var_tgts = []
    for obj in modified_objs:
        for rev_edge in globals.pt_graph.getRevEdgesFromSrouce(obj):
            if not isinstance(rev_edge.tgt,str): continue
            if not rev_edge.tgt.startswith("v_"): continue # ignore if not a variable
            if rev_edge.tgt not in var_tgts: var_tgts.append(rev_edge.tgt)
    for var_tgt in var_tgts:
        if var_tgt not in globals.var_to_encl_func: continue
        if globals.var_to_encl_func[var_tgt] not in result: result.append(globals.var_to_encl_func[var_tgt])

class SubscriptReadStmt(Stmt):
    def __init__(
             self,
             kind,
             encl_func,
             lhs,
             index,
             rhs
    ):
        super().__init__(kind,encl_func,lhs)
        self.index = index
        self.rhs = rhs
    def pretty_print(self):
        print("SubscriptRead in ",self.encl_func.name,self.lhs,"=",self.rhs,'['+str(self.index)+']')
    def solve(self):
        #self.pretty_print()
        change = False
        result = []
        for obj_Edge in globals.pt_graph.getEdgesFromSource(self.rhs):
            obj_id = obj_Edge.tgt
            if is_constant(obj_id): continue
            obj = globals.objects[obj_id]
            ref_index = _refine_index(self.index)
            if obj.kind == 'proto' and is_proto_container(obj):
                if ref_index == '*': 
                    exec_str = "for i in proto_list: result_list.append(proto_list[i])" if is_proto_container(obj,containers=("<class 'dict'>")) else "for i in proto_list: result_list.append(i)"
                    try:
                        locals = {'proto_list':obj.prototype,'result_list':[]}
                        #print("Printing locals:", locals)
                        #print("Subscript READ trying to exec...", exec_str,str(obj.prototype),type(obj.prototype),locals['result_list'])
                        exec(exec_str,None,locals)
                    except:
                        #print("Subscript * READ Threw an exception...", exec_str,str(obj.prototype),type(obj.prototype),locals['result_list'])
                        #self.pretty_print()
                        ...
                    for new_proto in locals['result_list']:
                        if globals.check_k_limit(self.lhs): break
                        #print("Here in Subscript READ, adding a new proto via the for loop:", new_proto)
                        change = globals.new_proto(obj.module_name,self.lhs,new_proto,self.encl_func) or change 
                else:
                    exec_str = "new_proto = proto_list[\'"+ref_index+"\']" if ins(ref_index,str) else "new_proto = proto_list["+str(ref_index)+"]"
                    try:
                        # No need to import env. Since we have gotten the proto object, that means env is on
                        locals = {'proto_list':obj.prototype}
                        exec(exec_str,None,locals)
                    except:
                        #print("Subscript READ Threw an exception...", exec_str,str(obj.prototype),type(obj.prototype))
                        #self.pretty_print()
                        continue    
                    if 'new_proto' not in locals: continue
                    if globals.check_k_limit(self.lhs): continue
                    new_proto = locals['new_proto']
                    #print("Here in Subscript READ, adding a new proto:", new_proto)
                    change = globals.new_proto(obj.module_name,self.lhs,new_proto,self.encl_func) or change                    
            if obj.kind == 'tuple_builtin' or obj.kind == 'list_builtin' or obj.kind == 'dict_builtin' or is_proto_container(obj): 
                for obj2_Edge in globals.pt_graph.getEdgesFromSource(obj_id):
                    obj2_id = obj2_Edge.tgt
                    index = obj2_Edge.label
                    if index == 'keys_list': continue
                    if ref_index == '*' or index == '*' or ref_index == index: 
                        #print("Adding edge ", self.lhs,obj2_id)
                        change = globals.pt_graph.addEdge(self.lhs,obj2_id,"") or change
        result = [self.encl_func] if change else []  
        return result
