import ast

import pt_engine.globals as globals
import pt_engine.datatypes as datatypes
import pt_engine.solvers.solver as solver
import pt_engine.solvers.call_stmt_solver as call_stmt_solver
import pt_engine.solvers.read_stmt_solver as read_stmt_solver

from ..utils.base import ins, obj_to_list, list_to_list, eval_with_return_in_extern, is_stmt, is_constant, encode_constant, decode_constant

# Generating 3-address code for function_def
# requires: called exactly once
def add_function_rep(module_obj,module_name,function_def,params):
  #print("\nAdding function rep for ",module_name,function_def.name)
  func_visitor = FunctionVisitor(module_obj,module_name,function_def,params)
  func_visitor.generic_visit(function_def)
  #print("Exiting function rep for ",module_name,function_def.name)

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self,module_obj,module_name,func_def,params):
      self.module_obj = module_obj
      self.module_name = module_name
      self.func_def = func_def
      self.gamma = params # Add parameters to local environment
      self.ret_vars = []
      self.gamma_map = {} # Maintain a mapping from locals to globally unique variable name
    
      globals.local_env[self.func_def] = self.gamma_map # Register local environment for this function
      self.create_kwarg_dict()
      self.process_defaults()
      self.process_keyword_defaults()
      for local in self.gamma: self.get_local_id(local)

    # effects: generates a fresh var name for local
    def get_local_id(self,local):
      if local not in self.gamma_map:
        self.gamma_map[local] = "v_"+str(globals.fresh_var(self.func_def))
      return self.gamma_map[local]

    # Requires: should be called after local var ids are created in gamma_map
    def create_kwarg_dict(self):
      if self.func_def.args.kwarg != None:
        kwarg = self.func_def.args.kwarg.arg
        # print("Here, found a new kwarg arg!!! ",self.func_def.name,kwarg)
        local_id = self.get_local_id(kwarg) 
        obj_id = "o_"+str(globals.fresh_obj())
        globals.objects[obj_id] = datatypes.Object(kind='dict_builtin',module_name=self.module_name)
        list_obj_id = "o_"+str(globals.fresh_obj())
        globals.objects[list_obj_id] = datatypes.Object(kind='list_builtin',module_name=self.module_name)
        globals.pt_graph.addEdge(local_id,obj_id,"")
        globals.pt_graph.addEdge(obj_id,list_obj_id,"keys_list")
    
    def process_defaults(self):
      # Processing defaults:
      if self.func_def.args.args == None or self.func_def.args.defaults == None:
        return # No defaults to assign
      f_args = self.func_def.args.args
      f_defaults = self.func_def.args.defaults
      i = len(f_args)-1
      for default in reversed(f_defaults):
        self.mark_stack()
        self.visit(default)
        default_values = self.pop_stack()
        param_i = f_args[i].arg # Extracting the name of the parameter
        self.process_default_const_assign(param_i,default_values)
        i = i-1
    
    # requires: formal is in local map, default is default_value, typially an ast.Constant, but can actually be anything
    # and we are processing just as an Assign 
    def process_default_const_assign(self,formal,default_values):
      # print("here default pairs: ", formal, default, " in ",self.func_def.name)
      formal_var = self.get_local_id(formal) 
      for default_var in default_values:
        #Track lineno. of lhs_var (vvv this will do!?) HERE?
        self.add_to_varid_to_lineno(formal_var, [globals.short_path(self.module_name), self.func_def.name, self.func_def.lineno, self.func_def.col_offset])
        impl_assign_stmt = solver.AssignStmt('Assign',self.func_def,formal_var,default_var)
        # print("!!! Adding an Assign stmt in ", self.func_def.name)
        # impl_assign_stmt.pretty_print()
        globals.add_stmt(self.func_def,impl_assign_stmt)
      
    def process_keyword_defaults(self):
      if self.func_def.args.kwonlyargs == None or self.func_def.args.kw_defaults == None:
        return # No keyword defaults to assign
      f_kwonlyargs = self.func_def.args.kwonlyargs
      f_kw_defaults = self.func_def.args.kw_defaults
      assert len(f_kwonlyargs) == len(f_kw_defaults)
      for keyword, kw_default in zip(f_kwonlyargs, f_kw_defaults):
        # print("HERE in kw!", keyword.arg, kw_default)
        # if "_init_" in self.func_def.name: print("Visiting the error expression", keyword.arg," = ", ast.unparse(kw_default))
        if kw_default == None:
          pass
        else:
          self.mark_stack()
          self.visit(kw_default)
          defaults = self.pop_stack()
          self.process_default_const_assign(keyword.arg,defaults)     

    # ----- STATEMENT VISITORS ------ #

    def visit_FunctionDef(self, node):
      #print("HERE in visit function def!, ", node.name)
      local_id = self.get_local_id(node.name)
      obj_to_list(node.name,self.gamma) # Adding name, as this is essentially an assignment creating a local var
      obj_id = "o_"+str(globals.fresh_obj())
      globals.objects[obj_id] = datatypes.Object("meta_func",func=node,module_name=self.module_name)
      globals.pt_graph.addEdge(local_id,obj_id,"")

    def visit_AsyncFunctionDef(self, node):
      #print("HERE in visit function def!, ", node.name)
      local_id = self.get_local_id(node.name)
      obj_to_list(node.name,self.gamma) # Adding name, as this is essentially an assignment creating a local var
      obj_id = "o_"+str(globals.fresh_obj())
      globals.objects[obj_id] = datatypes.Object("meta_func",func=node,module_name=self.module_name)
      globals.pt_graph.addEdge(local_id,obj_id,"")

    def visit_AugAssign(self, node):
     # This is target += value
     # print("\nAugAssign: ",ast.unparse(node))
     self.visit_Assign(ast.Assign(targets=[node.target],value=ast.BinOp(left=node.target,right=node.value,op=node.op),lineno=node.lineno))

    def visit(self, node):
      # We'll try evaluating each expression in extern
      # If success, set ret_vars to fresh proto
      # Otherwise, default to abstract eval by calling super.visit
      # Along with abstract eval, we'll attempt a concrete eval in the extern+local environment

      # print("Here in overriden visit, trying: ",ast.unparse(node))
      if is_stmt(node) or isinstance(node,(ast.Name,ast.Constant)):
        #print("--- stmt or name: ", ast.unparse(node))
        ast.NodeVisitor.visit(self,node)
        return
      #print("TRYING EVAL FOR", ast.unparse(node))
      extern = eval_with_return_in_extern(ast.unparse(node),self.module_obj.extern_env)
      if not (ins(extern,str) and extern == "None_Found"):
        # print("--- eval succeeds!",ast.unparse(node))
        fresh = "v_"+str(globals.fresh_var(self.func_def))   
        #print(self.func_def.name)
        globals.new_proto(self.module_name,fresh,extern,self.func_def)
        self.ret_vars += [fresh]
      else: 
        # print("--- eval fails: ",ast.unparse(node),type(node))
        ast.NodeVisitor.visit(self,node)
        # Now we'll try evaluating in local environment too
        locals = {}
        for local in self.gamma_map:
          for objEdge in globals.pt_graph.getEdgesFromSource(self.gamma_map[local]):
            tgt_obj_id = objEdge.tgt
            if is_constant(tgt_obj_id):
              locals[local] = decode_constant(objEdge.tgt)
              # print("Found a local constant: ", locals[local])
              continue
            tgt_obj = globals.objects[tgt_obj_id]
            if tgt_obj.kind == 'proto':
              locals[local] = tgt_obj.prototype
              # print("Found a local proto: ", tgt_obj.prototype)
              continue
        extern2 = eval_with_return_in_extern(ast.unparse(node),self.module_obj.extern_env,locals)
        if not (ins(extern2,str) and extern2 == "None_Found"):
          #print("SECOND EVAL SUCCEEDS? ",ast.unparse(node))
          fresh = "v_"+str(globals.fresh_var(self.func_def))   
          globals.new_proto(self.module_name,fresh,extern2,self.func_def)
          self.ret_vars += [fresh]

        
    def visit_AnnAssign(self, node):
      # print("\nAnnAssign: ",ast.dump(node, include_attributes=True));
      if node.value != None:
        self.visit_Assign(ast.Assign(targets=[node.target],value=node.value))

    def visit_Assign(self, node):
      # targets, value; can have tuple, e.g., x,y = f() and multiple targets x = y = f()                                                                  
      #if "_urllib_parse_moved_attributes" in ast.unparse(node.targets): print("\n!!! Assign: ",ast.dump(node));          
      self.mark_stack()
      self.visit(node.value)
      rhs_vars = self.pop_stack()
      for target in node.targets:
        for rhs_var in rhs_vars:
          assert ins(target,ast.Tuple) or ins(target,ast.List) or ins(target,ast.Attribute) or ins(target,ast.Name) or ins(target,ast.Subscript)
          if ins(target,ast.Tuple) or ins(target,ast.List):
            sub = 0
            for elem in target.elts:
              self._Assign_Helper(elem,rhs_var,sub) # indexed assign, will create a builtin tuple or a builtin list
              sub+=1
          elif ins(target,ast.Name) or ins(target,ast.Attribute) or ins(target,ast.Subscript):
            #if "_urllib_parse_moved_attributes" in ast.unparse(node.targets): print("\n!!! Assign: ",target.id, rhs_var); 
            self._Assign_Helper(target,rhs_var)
          else:
            pass

    # lhs is an ast.Node expression, rhs_var is an anlysis var
    def _Assign_Helper(self, lhs, rhs_var, index=None):
      # store in symbol table only if lhs is a Name                                                                                                           
      #print("Here in Assign Helepr recording lhs",lhs,rhs_var)                                                                                         
      # TODO: If lhs is a Name qualified with global, then we should not add to the local envirinment
      if ins(lhs,ast.Name):
        # Assuming a local
        if lhs.id not in self.gamma: 
          obj_to_list(lhs.id,self.gamma)  
        lhs_var = self.get_local_id(lhs.id)
        if index == None:
            # Do copy prop on the fly, will help concrete evaluation in extern+local:
            if is_constant(rhs_var):
              globals.pt_graph.addEdge(lhs_var,rhs_var,"")
              assign_stmt = solver.AssignStmt('Assign',self.func_def,lhs_var,rhs_var)
              globals.add_stmt(self.func_def,assign_stmt)
            else:   
              pt_targets = globals.pt_graph.getEdgesFromSource(rhs_var)
              if len(pt_targets) == 1:
                tgt_obj_id = pt_targets[0].tgt
                if is_constant(tgt_obj_id) or globals.objects[tgt_obj_id].kind == 'proto':
                  # print("Just added ",tgt_obj_id," due to copy prop")
                  globals.pt_graph.addEdge(lhs_var,tgt_obj_id,"")
              # Track lineno
              self.add_to_varid_to_lineno(lhs_var, [globals.short_path(self.module_name), self.func_def.name, lhs.lineno, lhs.col_offset])
              assign_stmt = solver.AssignStmt('Assign',self.func_def,lhs_var,rhs_var) # likely redundant
              #if lhs.id == "_urllib_parse_moved_attributes": assign_stmt.pretty_print()
              globals.add_stmt(self.func_def,assign_stmt)
        else:
            subscript_read = solver.SubscriptReadStmt('SubscriptRead',self.func_def,lhs_var,index=index,rhs=rhs_var)
            globals.add_stmt(self.func_def,subscript_read) 
      elif ins(lhs,ast.Attribute):
        self.mark_stack()
        self.visit(lhs.value)
        lhs_vars = self.pop_stack()
        for lhs_var in lhs_vars:
          update_stmt = solver.UpdateStmt('Update',self.func_def,lhs_var,rhs=rhs_var,fld=lhs.attr)
          #update_stmt.pretty_print()
          globals.add_stmt(self.func_def,update_stmt)
      elif ins(lhs,ast.Subscript):
        self.mark_stack()
        self.visit(lhs.value)
        lhs_vars = self.pop_stack()
        for lhs_var in lhs_vars:
          self.mark_stack()
          self.visit(lhs.slice)
          slice_vars = self.pop_stack()
          index = lhs.slice.value if ins(lhs.slice,ast.Constant) else slice_vars
          subscript_update = solver.SubscriptUpdateStmt('SubscriptUpdate',self.func_def,lhs_var,index=index,rhs=rhs_var)
          globals.add_stmt(self.func_def,subscript_update)
      elif ins(lhs,ast.Starred):
        pass
        # TODO: Add handling for Starred lhs
      else:
        pass
        # TODO: this is an error

    def visit_For(self, node):
      # for target in iter: body
      # print("visit For",ast.unparse(node),ast.dump(node))
      self.visit_Assign(ast.Assign(targets=[node.target],value=ast.Subscript(value=node.iter,slice=ast.Index(value=ast.Name(id="dummy_var"))),lineno=node.lineno))
      for stmt in node.body:
        # TODO: shall we surround by push/pop? Figure invariant of ret_vars.
        self.visit(stmt)

    # ------- EXPRESSIONS ------- #

    def visit_Name(self, node): 
      #print("Here in visit_Name: ",node.id)
      if node.id in self.gamma_map:
        # print("Should be right here in visit_Name now: ",node.id,self.gamma_map[node.id])
        # obj_to_list(self.gamma_map[node.id],self.ret_vars)
        self.ret_vars += [self.gamma_map[node.id]] # self.ret_vars is a STACK!!!
      else:
        # search for var in imports, return a tuple (full name, class def or func def)
        # add a pt edge
        result = []     
        for (full_var_name,new_node) in self.module_obj.search_name(node.id):
          # If node is a meta object that needs to be registered as var.
          if ins(new_node,ast.ClassDef) or ins(new_node,ast.FunctionDef) or ins(new_node,ast.AsyncFunctionDef):
            obj_to_list(globals.register_meta_object(full_var_name,new_node),result)
          else:
            # node is is a unique id, v_id actually
            assert new_node.startswith("v_"), full_var_name+" and node: "+new_node
            obj_to_list(new_node,result)
            #TODO: now we have to search for var in ???  
        #list_to_list(result,self.ret_vars)
        self.ret_vars += result 
        if result == []:
          # If result is [] we try evaluate to a built-in function  
          # Precedence of evaluation: first local env, then module initializers, then extern
          extern = eval_with_return_in_extern(ast.unparse(node),self.module_obj.extern_env)
          if not (ins(extern,str) and extern == "None_Found"):
            #print("Succeeded evaluating in Name: ",ast.unparse(node))
            globals.new_proto(self.module_name,node.id,extern,self.func_def)
            self.ret_vars += [node.id]

    def visit_Attribute(self, node):
      # print("\nAttribute: "+ast.unparse(node))
      # print("Extern env",self.module_obj.extern_env)
      fresh = "v_"+str(globals.fresh_var(self.func_def))
      # Process super().attr TODO: Add handling of argumeents to super. 
      if ins(node.value,ast.Call) and ins(node.value.func,ast.Name) and node.value.func.id == "super":
        # retrive self from env
        self_id = self.get_local_id("self")
        globals.add_stmt(self.func_def,read_stmt_solver.ReadStmt('Read',self.func_def,fresh,self_id,node.attr,is_super=True))
        self.ret_vars += [fresh]
        return
      # Try to resolve in package environment
      # if "error" in ast.unparse(node): print("And now here: Attribute: "+ast.unparse(node), self.module_name)
      result = self.module_obj.search_attribute(ast.unparse(node.value),node.attr)
      if result == []:
        # We will resolve in local env
        self.mark_stack()
        self.visit(node.value)
        rhs_vars = self.pop_stack()
        for rhs_var in rhs_vars:
          globals.add_stmt(self.func_def,read_stmt_solver.ReadStmt('Read',self.func_def,fresh,rhs_var,node.attr))
        self.ret_vars += [fresh]  
      else: 
        # Adding var name for meta object to stack
        for (full_var_name,new_node) in result:
          if ins(new_node,ast.ClassDef) or ins(new_node,ast.FunctionDef) or ins(new_node,ast.AsyncFunctionDef):
            obj_to_list(globals.register_meta_object(full_var_name,new_node),self.ret_vars)
          else:
            assert new_node.startswith("v_")
            #obj_to_list(node,self.ret_vars) #full_var_name is a var id
            self.ret_vars += [new_node]
         
    def visit_Call(self,node):
      #print("Call: ", ast.unparse(node))
      self.mark_stack()
      self.visit(node.func)
      funcs = self.pop_stack()
      args = []
      i = 0
      for arg in node.args:
        #print("arg[i]: ",ast.unparse(node.args[i]))
        if ins(arg,ast.Starred): # The *a delimiter vararg argument
          self.mark_stack()
          self.visit(arg.value) #node.args[i])
          arg_vars = self.pop_stack()
          # print("arg and arg_vars: ",ast.unparse(arg),ast.unparse(arg.value),arg_vars)
          # TODO: Revisit var arg. When formal in dummy test main funcs does not exist, visit does not push anything on list, it is empty.
          # What are implications of *arg, i.e., can it mess up argument count?
          if len(arg_vars) > 0: args.append(arg_vars[0]) # append as a Var, not a list
        else:
          self.mark_stack()
          self.visit(arg) #node.args[i])
          arg_vars = self.pop_stack()
          arg_i = []
          for arg_var in arg_vars: arg_i.append(arg_var)
          args.append(arg_i)
        i = i+1  
      kwargs = []  
      for keyword in node.keywords:
        # requires: These ought to be Name, value tuples where value can be an arbitrary expr
        # **kwargs is at the end. kwargs can be an arbitrary expression
        # Will be recorded as (None, kwargs)
        self.mark_stack()
        self.visit(keyword.value)
        values = self.pop_stack()
        kwargs.append((keyword.arg,values))
      assert ins(args,list), "Wrong call, args: "+ast.unparse(node)
      assert ins(kwargs,list), "Wrong call, kwargs: "+ast.unparse(node)
      # print("HERE, why is it missing?", ast.unparse(node))
      if not (ast.unparse(node.func) == 'dict' or ast.unparse(node.func) == 'list' or ast.unparse(node.func) == 'tuple'):
        fresh = "v_"+str(globals.fresh_var(self.func_def))
        self.ret_vars += [fresh]
        # print("Adding a Call stmt in ", self.func_def.name, ast.unparse(node))
        call_stmt = call_stmt_solver.CallStmt('Call',self.func_def,fresh,funcs,args,kwargs)
        #call_stmt.pretty_print()
        globals.add_stmt(self.func_def,call_stmt)
        #if funcs == []: print("\nEMPTY FUNCS!",self.func_def.name,self.module_name,ast.unparse(node))
      else:        
        # print("Processing a dict/list/tuple constructor call ", ast.unparse(node), ast.dump(node))
        # print("args: ",str(args))
        # dict/list/tuple is copied out from a prototype dict/list/tuple given as an argument
        fresh = self._create_builtin_object(ast.unparse(node.func)+'_builtin')
        self.ret_vars += [fresh]
        if kwargs == []:
          for arg_list in args:
            for container_var in arg_list:
              fresh2 = globals.fresh_var(self.func_def)
              index = ['dummy_var']
              subscript_read = solver.SubscriptReadStmt('SubscriptRead',self.func_def,fresh2,index=index,rhs=container_var)
              globals.add_stmt(self.func_def,subscript_read) 
              subscript_update = solver.SubscriptUpdateStmt('SubscriptUpdate',self.func_def,fresh,index=index,rhs=fresh2)
              globals.add_stmt(self.func_def,subscript_update)
        else:
          assert ast.unparse(node.func) == 'dict', "Incorrect container, not a dict "+ast.unparse(node.func)
          for (keyword,args) in kwargs:
            for arg in args:
              subscript_update = solver.SubscriptUpdateStmt('SubscriptUpdate',self.func_def,fresh,index=keyword,rhs=arg)



    def visit_Return(self,node):
      #self.ret_vars = [] # TODO: Is it []?
      if node.value == None: return
      self.mark_stack()
      self.visit(node.value)
      the_ret_vars = self.pop_stack()
      fresh = self.get_local_id(self.func_def.name+"_ret")
      for ret_var in the_ret_vars:
        # print("Adding a ret Assign stmt in ", self.func_def.name,fresh,ret_var)
        # Track lineno
        self.add_to_varid_to_lineno(fresh, [globals.short_path(self.module_name), self.func_def.name, node.lineno, node.col_offset])
        globals.add_stmt(self.func_def,solver.AssignStmt('Assign',self.func_def,fresh,ret_var))

    def visit_Constant(self,node):
      #print("Visiting constant: ", ast.dump(node))
      val = encode_constant(node.value)
      #obj_to_list(val,self.ret_vars)
      self.ret_vars += [val]

    def visit_Compare(self,node):
      self.mark_stack()
      self.generic_visit(node)
      self.pop_stack()
      # print("Compare before pop: ",self.ret_vars)
      self.ret_vars += ['c_bool_True','c_bool_False']
    
    def visit_BinOp(self,node):
      if ins(node.op,ast.Add):
        op = '+'
      elif ins(node.op,ast.Sub):
        op = '-'
      elif ins(node.op,ast.Mult):
        op = '*'
      elif ins(node.op,ast.Div):
        op = '/'
      elif ins(node.op,ast.MatMult):
        op = '@'
      else:
        op = "unsupported"
      if op == "unsupported":
        self.generic_visit(node)
      else:
        self.mark_stack()
        self.visit(node.left)
        lhsides = self.pop_stack()
        self.mark_stack()
        self.visit(node.right)
        rhsides = self.pop_stack()
        fresh = "v_"+str(globals.fresh_var(self.func_def))
        for lhs_var,rhs_var in zip(lhsides,rhsides): 
            # print("op and node.op", op,ast.unparse(node.op))
            binop_stmt = solver.BinOpStmt('Binop',self.func_def,fresh,lhs_var,rhs_var,op)
            #print("Adding an Binop stmt in ", self.func_def)
            #binop_stmt.pretty_print()
            globals.add_stmt(self.func_def,binop_stmt)
        self.ret_vars += [fresh]
    
    # BUILTIN OBJECT EXPRESSIONS

    def _create_builtin_object(self,kind):
      #fresh = "v_"+str(globals.fresh_var())
      fresh = "v_"+str(globals.fresh_var(self.func_def))
      obj_id = "o_"+str(globals.fresh_obj())
      globals.objects[obj_id] = datatypes.Object(kind=kind,module_name=self.module_name)
      globals.pt_graph.addEdge(fresh,obj_id,"")
      if kind == 'dict_builtin':
        list_obj_id = "o_"+str(globals.fresh_obj())
        globals.objects[list_obj_id] = datatypes.Object(kind='list_builtin',module_name=self.module_name)
        globals.pt_graph.addEdge(obj_id,list_obj_id,"keys_list")
      return fresh

    def _create_builtin_object_UNUSED(self,kind):
      # Purpose of this is to "link" builtin to stub in typeshed, eventually add summaries.
      # 1. find tuple class in threashold module
      # 2. get full name
      # 3. meta_tuple = globals.register_meta_object(full_name,node)
      # 4. add a call stmt
      for node in globals.typeshed_builtins_module.classes:
        if node.name == kind[:-8]:
          cls_node = node
      meta_cls = globals.register_meta_object(globals.typeshed_builtins_module.path+":"+kind[:-8],cls_node)
      fresh = "v_"+str(globals.fresh_var(self.func_def))
      obj_id = "o_"+str(globals.fresh_obj())
      globals.objects[obj_id] = datatypes.Object(kind=kind,cls_meta_obj=meta_cls,module_name=self.module_name)
      globals.pt_graph.addEdge(fresh,obj_id,"")
      if kind == 'dict_builtin':
        list_obj_id = "o_"+str(globals.fresh_obj())
        globals.objects[list_obj_id] = datatypes.Object(kind='list_builtin',module_name=self.module_name)
        globals.pt_graph.addEdge(obj_id,list_obj_id,"keys_list")
      return fresh

    def visit_Tuple(self,node):
      fresh = self._create_builtin_object('tuple_builtin')
      self._tuple_update(node.elts,fresh)
      self.ret_vars += [fresh]

    def _tuple_update(self,node_elts,lhs):
      index = 0
      for elem in node_elts:
        self.mark_stack()
        self.visit(elem)
        elems = self.pop_stack()
        for ret_var in elems:
          subscript_update = solver.SubscriptUpdateStmt('SubscriptUpdate',self.func_def,lhs,index=index,rhs=ret_var)
          globals.add_stmt(self.func_def,subscript_update) 
        index = index+1
    
    def _dict_update(self,node_keys,node_values,lhs):
        for key,val in zip(node_keys,node_values):
          #print(key.__repr__(),val.__repr__())
          self.mark_stack()
          self.visit(val)
          rhs_vars = self.pop_stack()
          if key == None: 
            for rhs_var in rhs_vars:
              stmt_to_add = solver.AssignStmt("Assign",self.func_def,lhs,rhs_var)
              # print("dict_update Assign: ")
              # stmt_to_add.pretty_print()
              globals.add_stmt(self.func_def,stmt_to_add) 
          else: 
            self.mark_stack()
            self.visit(key)
            key_vars = self.pop_stack()
            index = key.value if ins(key,ast.Constant) else key_vars
            for rhs_var in rhs_vars:
              stmt_to_add = solver.SubscriptUpdateStmt('SubscriptUpdate',self.func_def,lhs,index=index,rhs=rhs_var)
              # print("dict_update Subscript Update: ")
              # stmt_to_add.pretty_print()
              globals.add_stmt(self.func_def,stmt_to_add) 
          
    def visit_Dict(self,node):
      fresh = self._create_builtin_object('dict_builtin')
      list_obj_id = "o_"+str(globals.fresh_obj())
      # print("Here in Dict:", self.func_def.name, ast.unparse(node))
      self._dict_update(node.keys,node.values,fresh)
      self.ret_vars += [fresh]

    def visit_List(self,node):
      fresh = self._create_builtin_object('list_builtin')
      self._tuple_update(node.elts,fresh)
      self.ret_vars += [fresh]

    def visit_Subscript(self,node):
      # print("Visiting subscript",ast.unparse(node))
      fresh = "v_"+str(globals.fresh_var(self.func_def))
      self.mark_stack()
      self.visit(node.value)
      rhs_vars = self.pop_stack()
      for rhs_var in rhs_vars:
        #index = str(node.slice.value) if ins(node.slice,ast.Constant) else '*'
        self.mark_stack()
        self.visit(node.slice)
        # print("And slice before,", ast.unparse(node.slice),type(node.slice))
        slice_vars = self.pop_stack()
        index = node.slice.value if ins(node.slice,ast.Constant) else slice_vars
        # print("And here before setting the subscript read ",index)
        subscript_read = solver.SubscriptReadStmt('SubscriptRead',self.func_def,fresh,index=index,rhs=rhs_var)
        # print("Here in visit_Subscript:", ast.unparse(node))
        # subscript_read.pretty_print()
        globals.add_stmt(self.func_def,subscript_read) 
      self.ret_vars += [fresh]

    def visit_ListComp(self,node):
      for comp in node.generators:
        assign_stmt = ast.Assign(targets=[comp.target],value=ast.Subscript(value=comp.iter,slice=ast.Index(value=ast.Name(id="dummy_var"))),lineno=node.lineno)
        self.visit_Assign(assign_stmt)
        for if_expr in comp.ifs:
          self.mark_stack()
          self.visit(if_expr)
          self.pop_stack()
      fresh = self._create_builtin_object('list_builtin')
      self._tuple_update([node.elt],fresh)  
      self.ret_vars += [fresh]    

    def visit_DictComp(self,node):
      # print("Here in DictComp trying ", ast.unparse(node), ast.dump(node), self.func_def.name,self.module_name)
      for comp in node.generators:
        rhs_value = ast.Subscript(value=comp.iter,slice=ast.Index(value=ast.Name(id='dummy_var')))
        assign_stmt = ast.Assign(targets=[comp.target],value=rhs_value,lineno=node.lineno)
        # print("Here in DictComp: ",ast.unparse(node), ast.unparse(assign_stmt))
        # print(ast.dump(node))
        self.visit_Assign(assign_stmt)
        for if_expr in comp.ifs:
          self.mark_stack()
          self.visit(if_expr)
          self.pop_stack()
      fresh = self._create_builtin_object('dict_builtin')
      self._dict_update([node.key],[node.value],fresh)
      self.ret_vars += [fresh]
    
    def visit_Raise(self,node):
      if isinstance(node.exc, ast.Call):
        self.visit_Call(node.exc)
        #print(ast.dump(node.exc))
        #assert False
      #self.generic_visit(node)

    '''
    TODO: Add generators. 
    def visit_GeneratorExp(self,node):
      print("Gen comp:", ast.unparse(node))
      print("Gen comp elt:",ast.unparse(node.elt))
      print("Gen comp generators:",type(node.generators[0].iter), ast.unparse(node.generators[0].iter))
      exit(1)
    '''  

    def mark_stack(self):
      self.ret_vars.append("MARKER")

    def pop_stack(self):
      result = []
      #print("Compare before pop: ",self.ret_vars)
      while self.ret_vars[-1] != "MARKER":
        result.append(self.ret_vars[-1]) 
        self.ret_vars = self.ret_vars[:-1]
      #print("Compare after pop: ",self.ret_vars)
      self.ret_vars = self.ret_vars[:-1]
      return result


    # BEW
    # add to varid_to_lineno dict
    # value = [file_path, func_name, line no, col offset]
    def add_to_varid_to_lineno(self, var_id, value):
      if var_id in globals.varid_to_lineno:
        ll = globals.varid_to_lineno[var_id]
        ll.append(value)
        globals.varid_to_lineno[var_id] = ll
      else:
        globals.varid_to_lineno[var_id] = value
