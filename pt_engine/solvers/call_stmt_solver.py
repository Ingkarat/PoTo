import ast

import pt_engine.globals as globals
import pt_engine.datatypes as datatypes
import pt_engine.visitors.function_visitor as function_visitor

from ..solvers.stmt import Stmt, solve_proto_call

from ..utils.base import ins, maybe_to_list, is_decorator, obj_to_list, list_to_list, is_constant

class CallStmt(Stmt):
    def __init__(
             self,
             kind,
             encl_func,
             lhs,
             funcs,
             args,
             kwargs
    ):
        super().__init__(kind,encl_func,lhs)
        self.funcs = funcs
        self.args = args
        self.kwargs = kwargs
        self.hash = 0
    def pretty_print(self):
        # Processes a call statement: v_lhs = v_funcs(v_args,v_kwargs)
        print("Call:",self.lhs," = ",self.funcs,"(",str(self.args),str(self.kwargs),")")
    def hash_fun(self):
        result = 0
        for func in self.funcs:
            result += 1 if is_constant(func) else len(globals.pt_graph.getEdgesFromSource(func))
        for arg_list in self.args:
            for arg in arg_list:
                result += 1 if is_constant(arg) else len(globals.pt_graph.getEdgesFromSource(arg))   
        for kwarg in self.kwargs:
            for karg in kwarg[1]:
                result += 1 if is_constant(karg) else len(globals.pt_graph.getEdgesFromSource(karg))  
        return result
                
    def solve(self):
        result = []
        #print("Here in solve of Call ", self.encl_func.name)
        #self.pretty_print()
        if self.hash == self.hash_fun(): return [] # Nothing changed since last time we saw this
        for func in self.funcs:
            #if (func == 'max'): print("Evaluating self.funcs ", func)
            #print(func, "and size", len(globals.pt_graph.getEdgesFromSource(func)))
            for obj_edge in globals.pt_graph.getEdgesFromSource(func):
                if is_constant(obj_edge.tgt): continue
                obj = globals.objects[obj_edge.tgt]
                #print("Pretty printing function object:")
                #obj.pretty_print()
                res = []
                #obj.pretty_print()
                if obj.kind == 'meta_cls': # This is a "new" statement: Cls(a,b,c)
                    #if (func == 'dir'): print("Arm 1, meta_cls: ", func)
                    res = self._solve_meta_cls_receiver(obj)
                elif obj.kind == 'meta_func': # This is a closure call: func(a,b,c) where func may be a closure (bound method in Python speak)
                    #if (func == 'dir'): print("Arm 2, meta_func: ", func)
                    res = self._solve_meta_func_receiver(obj)
                elif obj.kind == 'proto':
                    #print('Evaluating a proto object ...')
                    #if (func == 'open'): print("Arm 3, proto: ", func)
                    res = solve_proto_call(obj,self.args,self.lhs,self.encl_func,'(',')')
                elif obj.kind == 'user':
                    #if (func == 'dir'): print("Arm 4, user: ", func)
                    # TODO: Need to handle __call__ search
                    pass
                else:
                    #if (func == 'dir'): print("Arm 5, pass: ", func)
                    pass
                list_to_list(res,result)
        self.hash = self.hash_fun()        
        return result
    
    # equivalent to lhs = new Cls()
    def _solve_meta_cls_receiver(self,obj): 
        assert obj.kind == 'meta_cls'
        o_user_obj = _find_user_obj(self.lhs,obj.cls)
        #print(">>> ", type(o_user_obj), type(obj))
        obj_creation = False
        if o_user_obj==None: # Need to create the new user object
            o_user_obj = "o_"+str(globals.fresh_obj())
            globals.objects[o_user_obj] = datatypes.Object('user',cls_meta_obj=obj)
            globals.pt_graph.addEdge(self.lhs,o_user_obj,"") # No annotation on edge
            # Have to add current function to result as pt set has changed.
            obj_creation = True
        init_func = _find_function_def(obj.cls,"__init__")
        # There is no meta_func object for 
        if init_func == None: return [] 
        # Register the init func
        # globals.module_names[init_func] = globals.module_names[obj.cls] #obj.module_name
        #tgt_encl_path = obj.module_name + ":" + obj.cls.name
        res = _processCall([o_user_obj]+self.args,self.kwargs,init_func,self.lhs,self.encl_func)
        if obj_creation: obj_to_list(self.encl_func,res)
        return res
    
    def _solve_meta_func_receiver(self,obj):
        #assert obj.kind == 'meta_func'
        globals.module_names[obj.func] = obj.module_name
        if is_decorator(obj.func,'classmethod'): return [] 
        if is_decorator(obj.func,'classmethod'):
            assert len(obj.closure_bindings)==1
            closure_bindings = [] # TODO: Fix this. Now ignoring classmethods
        elif is_decorator(obj.func,'staticmethod'):
            closure_bindings = []
        else:
            closure_bindings = maybe_to_list(obj.closure_bindings)        
        #tgt_encl_path = obj.module_name + ":" + obj.func.name
        res = _processCall(closure_bindings+self.args,self.kwargs,obj.func,self.lhs,self.encl_func)
        return res
    
    '''
    # When func object is a prototype, we invoke fully instantiated calls
    # TODO: Right now, we completely ignore kwargs. It is possible that a library/builtin passes kwargs
    def _solve_proto_call(self,calee_proto,args,lhs,encl_func,left_paren,right_paren):
    #def _solve_proto_call(self, args, kwargs, calee_proto, lhs):

        #print("Starting solve proto ", calee_proto.prototype, self.args, self.kwargs)
                        
        change = False
        # Filter arguments to sets of proto and consts 
        filtered = globals.filter(args)
        if filtered == None: return [] # no concrete args to evaluate
        # Restructure into arg-value pairs to feed to call
        filtered = globals.cart_prod(filtered)
        # print("After card_prod", filtered)
        for arg_list in filtered:
            # print("arg_list", arg_list,len(arg_list))
            exec_str = 'calee_proto.prototype'+left_paren
            i = 0
            for arg in arg_list:
                arg_to_append = arg if ins(arg,str) else 'arg_list['+str(i)+']'
                exec_str = exec_str+arg_to_append+',' if i<len(arg_list)-1 else exec_str+arg_to_append 
                i=i+1     
            exec_str = exec_str+right_paren    
            exec_str = "new_proto = "+exec_str
            try:
                locals = {'calee_proto':calee_proto,'arg_list':arg_list}
                # print("Executing in call in",self.encl_func.name,exec_str)
                exec(exec_str,None,locals)
            except:
                #print("Threw an exception...", exec_str,calee_proto.prototype)
                #self.pretty_print()
                pass
            if 'new_proto' not in locals: continue # Call threw an exception
            if globals.check_k_limit(lhs): continue
            new_proto = locals['new_proto']
            #print("Here, and the result is ", new_proto)
            change = globals.new_proto(globals.module_names[encl_func],lhs,new_proto) or change

        result = [encl_func] if change else []
        return result
    '''

# Traverses pt set of a var to find user object of class def type
def _find_user_obj(var,class_def):
    for o_obj in globals.pt_graph.getEdgesFromSource(var):
        obj = globals.objects[o_obj.tgt]
        if obj.kind == 'user' and obj.cls_meta_obj.cls == class_def:
            return o_obj.tgt
    return None        

# Traverses body of class hierarchy in MRO order to find func_name
def _find_function_def(class_def,func_name):
    for cls in globals.mros[class_def]:
        for elem in cls.body:
            # print("Here in _find_function_def",func_name,cls.name)
            # print(ast.unparse(elem))
            if (ins(elem,ast.FunctionDef) or ins(elem,ast.AsyncFunctionDef)) and elem.name == func_name:
                globals.encl_class[elem] = cls # For pretty printing call graph
                # Now registering the function's module name
                globals.module_names[elem] = globals.module_names[cls]
                return elem
    return None

# --- Processing of actual to formal params, including **kwargs ---- #

# formal = act
def _process_act_to_formal(formal,act,calee_def):
    # print("In _process_act",formal,"=",act,calee_def.name,globals.module_names[calee_def])
    change = False

    # This happens only when processing a file of auto-generated fake main functions for testing.
    if formal not in globals.local_env[calee_def]: return change

    formal_var = globals.local_env[calee_def][formal]
    if "o_" in act:
        assert formal=='self', 'In method '+calee_def.name+":"+globals.objects[act].kind
        return globals.pt_graph.addEdge(formal_var,act,"")
    elif ins(act,list):      
        assert ins(act,list), 'act is not a list'+','+act
        for act_var in act: # act is a list that we have to traverse
            # print("--- Processing: ",formal_var,"=",act_var)
            change = globals.x_eq_y(formal_var,act_var) or change
        return change
    else: 
        # TODO: this will happen if the actual act is a *args expansion. Still not handled
        return change
    
def _processCall(args, kwargs, calee_def, lhs, encl_func):

    #if "typeshed" in globals.module_names[calee_def]: print("Found a typeshed func: ", calee_def.name)

    assert ins(args,list), encl_func.name+"->"+calee_def.name
    # print("HERE in _processCall", args, kwargs, calee_def.name, lhs)
    result = []

    # Retrieving formals
    f_posonlyargs = calee_def.args.posonlyargs
    f_args = calee_def.args.args
    f_vararg = calee_def.args.vararg
    f_kwonlyargs = calee_def.args.kwonlyargs
    f_kwarg = calee_def.args.kwarg

    # Sorting out formals
    params = []
    arg_params = []
    kw_params = []
    vararg_list = [] if f_vararg == None else [f_vararg]
    kwarg_list = [] if f_kwarg == None else [f_kwarg]
    for arg in f_posonlyargs+f_args+vararg_list+f_kwonlyargs+kwarg_list: params.append(arg.arg)
    for arg in f_posonlyargs+f_args+vararg_list: arg_params.append(arg.arg)
    for arg in f_kwonlyargs+kwarg_list: kw_params.append(arg.arg)

    # TODO: Check params match
    
    #print("HERE just before calee_def...", calee_def.name)
    change = False
    # If calee is Not in reachable methods, invoke FunctionVisitor
    if calee_def not in globals.stmts:
        #print("(_processCall) Callee def name", calee_def.name)
        # print(ast.unparse(calee_def), "\n")
        module_name = globals.module_names[calee_def]
        module_obj = globals.package_env[module_name]
        function_visitor.add_function_rep(module_obj,module_name,calee_def,params)
        change = True
        # Add call graph edge
        globals.call_graph.addEdge(encl_func,calee_def,[lhs])
        globals.mirror_call_graph.addEdge(encl_func,calee_def,[lhs])
    else: # TODO: Code review this... Yeah, should have done it earlier not debugging :(
        found = False
        for call_edge in globals.call_graph.getEdgesFromSource(encl_func):
            # Case 1: there is a call in this same caller:
            if call_edge.tgt == calee_def:
                if lhs not in call_edge.label: call_edge.label.append(lhs) 
                found = True
        if not found:
            globals.call_graph.addEdge(encl_func,calee_def,[lhs])
            globals.mirror_call_graph.addEdge(encl_func,calee_def,[lhs])

    # Add parameters, if param changes, add calee to result
    count = 0
    for actual in args:
        # String can be v_x vararg or o_x for a receiver object
        # print("actual...",actual)
        assert ins(actual,list) or ins(actual,str), "processCall: Actual is not a list or string"
        if count >= len(arg_params): break # Matching the vararg param with the rest... TODO
        change = _process_act_to_formal(arg_params[count],actual,calee_def) or change
        count = count+1
    for (keyword,value_list) in kwargs:
        if keyword == None:
            # print("HERE kwarg?", calee_def.name,keyword,value_list,f_kwarg)
            assert len(value_list) == 1 # The kwarg arg
            kwarg_var = value_list[0] 
            for kwonlyarg in f_kwonlyargs:
                # Adding kw_var = kwarg_var[keword] actual to formal assignment
                kw_var = globals.local_env[calee_def][kwonlyarg.arg]
                change = globals.x_eq_y_f(kw_var,kwarg_var,kwonlyarg.arg) or change
            if f_kwarg != None:
                kwarg_param_var = globals.local_env[calee_def][f_kwarg.arg]
                change = globals.x_eq_y(kwarg_param_var,kwarg_var) or change
        elif (keyword in kw_params) or (keyword in arg_params): # It is a keyword only arg and an arg was passed
            change = _process_act_to_formal(keyword,value_list,calee_def) or change # pass the new arg
        else:
            # print("HERE kwarg?", calee_def.name,keyword,value_list,f_kwarg)
            # assert f_kwarg != None # TODO: Revisit. I don't think this is crucial but have to get to the bottom of it
            if f_kwarg == None: continue
            # Keyword is passed into **kwarg param: kwarg[keyword] = value_list
            kwarg_var = globals.local_env[calee_def][f_kwarg.arg]
            for val in value_list:
                change = globals.x_f_eq_y(kwarg_var,val,keyword) or change
    if change == True: 
        if calee_def not in result: result.append(calee_def)
    
    ''' # Moved this to assign stmt to optimize
    # Propagate ret -> lhs
    change = False
    if calee_def.name+"_ret" in globals.local_env[calee_def]:
        ret_var = globals.local_env[calee_def][calee_def.name+"_ret"]
        # print("Here tying up ret of",calee_def.name,"it is",ret_var,lhs)
        change = globals.x_eq_y(lhs,ret_var) or change
        
    if change == True:
        if encl_func not in result: result = [encl_func]+result
    '''
    return result         

'''
# TODO: Need abstract handlers: getattr, keys,values,items of Dict,  
# TODO: constructors, dict, list, tuple
'''