import pt_engine.globals as globals

class Stmt:
    '''
    Attributes
    ----------
      kind : One of ['Assign','Call','Update','Read','BinOp']
      lhs : optional str
      rhs : optional str
      fld : optional str
      encl_method : ast.FunctionDef
      args : optional List(str)

    '''
    def __init__(
             self,
             kind,
             encl_func,
             lhs
    ):
        self.kind = kind
        self.lhs = lhs
        self.encl_func = encl_func
    
    def pretty_print(self):
        print("Uknown kind of statement: ",self.kind)   

# Searches properties and returns func_str (setter or getter) function
def find_property(meta_cls_obj, prop_str : str, func_str : str):
    assert func_str == 'setter' or func_str == 'getter'
    if meta_cls_obj in globals.properties: # Yes properties data associated with runtime type
      if prop_str in globals.properties[meta_cls_obj] and func_str in globals.properties[meta_cls_obj][prop_str]: # No setter method
          method_def = globals.properties[meta_cls_obj][prop_str][func_str]
          return method_def
    return None

# TODO: Move back to call_stmt_solver
# Evaluates a proto call
# When func object is a prototype, we invoke fully instantiated calls
# TODO: Right now, we completely ignore kwargs. It is possible that a library/builtin passes kwargs
def solve_proto_call(calee_proto,args,lhs,encl_func,left_paren,right_paren):
  #def _solve_proto_call(self, args, kwargs, calee_proto, lhs):

  #print("Starting solve proto ", calee_proto.prototype, self.args, self.kwargs)
                  
  change = False
  # Filter arguments to sets of proto and consts 
  filtered = globals.filter(args)
  non_empty_proto_call = False
  if filtered != None: # We will attempt evaluation when there is at least one combination of concrete arguments
    # Restructure into arg-value pairs to feed to call
    filtered = globals.cart_prod(filtered)
    # print("After card_prod", filtered)
    for arg_list in filtered:
      #print("arg_list", arg_list,len(arg_list))
      exec_str = 'calee_proto.prototype'+left_paren
      i = 0
      for arg in arg_list:
          arg_to_append = arg if isinstance(arg,str) else 'arg_list['+str(i)+']'
          exec_str = exec_str+arg_to_append+',' if i<len(arg_list)-1 else exec_str+arg_to_append 
          i=i+1     
      exec_str = exec_str+right_paren    
      exec_str = "new_proto = "+exec_str
      if "function open" in str(calee_proto.prototype): continue
      if "read" in str(calee_proto.prototype): continue
      if "exit" in str(calee_proto.prototype): continue
      if "close" in str(calee_proto.prototype): continue
      if "split" in str(calee_proto.prototype): continue
      if "poll" in str(calee_proto.prototype): continue
      if "write" in str(calee_proto.prototype): continue
      if "vars" in str(calee_proto.prototype): continue
      try:
          locals = {'calee_proto':calee_proto,'arg_list':arg_list}
          #print("EXEC in call in",encl_func.name,exec_str,calee_proto.prototype)
          exec(exec_str,None,locals)
      except:
          #print("Threw an exception...", exec_str,calee_proto.prototype)
          #self.pretty_print()
          pass
      if 'new_proto' not in locals: continue # Call threw an exception
      non_empty_proto_call = True
      if globals.check_k_limit(lhs): continue
      new_proto = locals['new_proto']
      #print("Here, and the result is ", new_proto)
      change = globals.new_proto(globals.module_names[encl_func],lhs,new_proto,encl_func) or change

  if non_empty_proto_call == False:
      change = builtin_proto_call(calee_proto,args,lhs,encl_func) or change
  result = [encl_func] if change else []
  return result

# Will evaluate a builtin on abstract args
def builtin_proto_call(calee_proto,args,lhs,encl_func):
    #print("Couldn't evaluate proto call: ", calee_proto.prototype, args, " in ", encl_func.name)
    int_protos = ["built-in function len", "built-in function hash"]
    str_protos = ["built-in method join", "built-in method format", "built-in method replace"]
    bool_protos = ["built-in function isinstance", "built-in function issubclass"]
    float_protos = ["built-in function max","built-in function min","built-in function sin","built-in function cos","built-in function abs","built-in function sqrt","built-in function log"]
    (change,builtin_proto) = (False,False)
    (change,builtin_proto) = builtin_proto_call_exec('the_ret = 1',calee_proto,int_protos,lhs,encl_func,change,builtin_proto)
    (change,builtin_proto) = builtin_proto_call_exec("the_ret = 'msg'",calee_proto,str_protos,lhs,encl_func,change,builtin_proto)
    (change,builtin_proto) = builtin_proto_call_exec('the_ret = True',calee_proto,bool_protos,lhs,encl_func,change,builtin_proto)
    (change,builtin_proto) = builtin_proto_call_exec('the_ret = 1.0',calee_proto,float_protos,lhs,encl_func,change,builtin_proto)

    #if not builtin_proto: print("Couldn't evaluate proto call: ", calee_proto.prototype, args, " in ", encl_func.name)    
    return change

def builtin_proto_call_exec(exec_str,calee_proto,proto_list,lhs,encl_func,change,builtin_proto):
    for proto in proto_list:
        if proto in str(calee_proto.prototype):
            locals = {}
            exec(exec_str,None,locals)
            change = globals.new_proto(globals.module_names[encl_func],lhs,locals['the_ret'],encl_func) or change
            builtin_proto = True
    return (change, builtin_proto)

'''
def is_proto_container(obj,containers=("<class 'dict'>","<class 'list'>","<class 'tuple'>")):
    result = False
    if obj.kind == 'proto':
        locals = {'obj':obj}
        exec('type_of = type(obj.prototype)',locals)
        type_of = locals['type_of']
        if str(type_of) in containers:
            result = True
    return result 
'''
    