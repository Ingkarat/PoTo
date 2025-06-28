import ast
import os
import sys

# Side effects key_to_pt_type!
class ShallowInferVisitor(ast.NodeVisitor):
    def __init__(self,file_name,package_name,reachable_methods,type_map):
        self.file_name = file_name
        self.package_name = package_name
        self.reachable_methods = reachable_methods
        self.module = None
        self.class_name = None
        self.func_name = None
        self.type_map = type_map

    # If shallow-infer "type" for expr_node, add lhs_str -> type to self.type_map 
    def _analyze_expr(self,lhs_str,expr_node):
            if isinstance(expr_node,ast.JoinedStr):
               self._add_to_map(lhs_str,"str")
            if isinstance(expr_node,ast.Constant):
                if ast.unparse(expr_node) == 'True' or ast.unparse(expr_node) == 'False':
                   #print("Found a bool CONSTANT!", lhs_str, ast.unparse(expr_node))
                   self._add_to_map(lhs_str,"bool")
                elif isinstance(expr_node.value,int):
                   #print("Found an int CONSTANT!", lhs_str, ast.unparse(expr_node))
                   self._add_to_map(lhs_str,"int")
                elif isinstance(expr_node.value,str):
                   #print("Found an str CONSTANT!", lhs_str, ast.unparse(expr_node)) 
                   self._add_to_map(lhs_str,"str")  
            elif isinstance(expr_node,ast.List):
                self._add_to_map(lhs_str,"list")
                #print("Found a LIST!", lhs_str, ast.unparse(expr_node))
            elif isinstance(expr_node,ast.Dict):
                self._add_to_map(lhs_str,"dict")
                #print("Found a DICT!", lhs_str, ast.unparse(expr_node))
            elif isinstance(expr_node,ast.Tuple):
                self._add_to_map(lhs_str,"tuple")
                #print("Found a TUPLE!", lhs_str, ast.unparse(expr_node))    
            elif isinstance(expr_node,ast.GeneratorExp):
                self._add_to_map(lhs_str,"generator")
                #print("Found a TUPLE!", lhs_str, ast.unparse(expr_node)) 
            elif isinstance(expr_node,ast.Name):
                # simple propagation
                full_name = "('"+self.file_name + "', '"+self.func_name+"', '"+expr_node.id+"')"
                if full_name in self.type_map:
                   for tp in self.type_map[full_name]:
                      self._add_to_map(lhs_str,tp)
            elif isinstance(expr_node,ast.Compare):
                self._add_to_map(lhs_str,"bool")
            elif isinstance(expr_node,ast.Call):
                int_protos = ["len", "hash", "int", "int.from_bytes"]
                str_protos = ["join", "format", "replace", "str"]
                bool_protos = ["isinstance", "issubclass", "bool"]
                #if self.func_name == '__repr__':
                #   print("__repr__", ast.unparse(expr_node))
                func_str = ast.unparse(expr_node.func)
                if func_str in int_protos: self._add_to_map(lhs_str,"int")
                elif func_str in str_protos: self._add_to_map(lhs_str,"str")
                elif func_str in bool_protos: self._add_to_map(lhs_str,"bool")
                elif func_str == 'tuple': self._add_to_map(lhs_str,"tuple")
                elif func_str == 'dict': self._add_to_map(lhs_str,"dict")
                elif func_str == 'list': self._add_to_map(lhs_str,"list")
                elif func_str == 'set': self._add_to_map(lhs_str,"set")   
                if isinstance(expr_node.func,ast.Attribute):
                   if isinstance(expr_node.func.value,ast.Name) and expr_node.func.value.id == 'self':
                     # TODO: local propagation of return types at self.func_name(args). Will knock off several cases.
                     pass
                   if expr_node.func.attr in str_protos:
                     self._add_to_map(lhs_str,"str") # TODO: check value; unlikely but it could be an independent func "format"
            # TODO: collect more: use typeshed, use annotations?
    
    def _add_to_map(self,local_name,type_name,asynch=False):
        if self.func_name == None: # then it's either class initializer or module initializer
           if self.class_name == None:
              func_name = "module_initializer"
           else:
              func_name = self.class_name+"_class_initializer"
        else:
           func_name = self.func_name  
        if asynch == True:
           var_name = "('"+self.file_name + "', '"+local_name[:-4]+"', '"+local_name+"')"
        else:         
           var_name = "('"+self.file_name + "', '"+func_name+"', '"+local_name+"')"   
        # var_name = "('"+self.file_name + "', '"+self.func_name+"', '"+local_name+"')"
        if var_name not in self.type_map: self.type_map[var_name] = []
        if type_name not in self.type_map[var_name]: self.type_map[var_name].append(type_name)
        if type_name == "coroutine": 
            #print("Adding a coroutine type to ", var_name)
            ...

    def visit_Name(self,node):
       if node.id == 'self' and self.class_name != None:
        self._add_to_map('self',self.class_name)
        
    def visit_arg(self,node):
       if node.arg == 'self' and self.class_name != None:
        #print("OFFENDING node:",ast.unparse(node),self.class_name)
          self._add_to_map('self',self.class_name)
       if hasattr(node,"annotation") and node.annotation != None:
          #print("Here adding arg annotation: ",self.func_name, node.arg, ast.unparse(node.annotation))
          self._add_to_map(node.arg,"ANNO:"+ast.unparse(node.annotation)) 
 
    def visit_Assign(self,node):
        if self.func_name == None: return
        if len(node.targets) == 1 and isinstance(node.targets[0],ast.Name):
            self._analyze_expr(node.targets[0].id,node.value)
        self.generic_visit(node)    

    def visit_AnnAssign(self,node):
        # Adding the annotation 
        # print("here in ann assign, adding annotation ", ast.unparse(node))
        # assert isinstance(node.target,ast.Name), ast.unparse(node.target)+" is not a Name"
        if isinstance(node.target,ast.Name):
            self._add_to_map(node.target.id,"ANNO:"+ast.unparse(node.annotation))
        self.generic_visit(node)

    def visit_AugAssign(self,node):
        self.generic_visit(node)

    def visit_Return(self,node):
        if self.func_name == '__repr__':
            #print("__repr__", ast.dump(node))
            ...
        if node.value != None:
            self._analyze_expr(self.func_name+"_ret",node.value)
            self.generic_visit(node)

    def visit_ClassDef(self,node):
        self.class_name = node.name
        self.generic_visit(node)
        self.class_name = None

    def visit_FunctionDef(self,node):
        # TODO: Can add default argument types
        # TODO: For now returning if entering a nested fuction as we do not collect nested funcs for pytype. URGENT
        if self.func_name != None: return   
        meth_name = "('"+self.file_name + "', '"+node.name+"')"
        #print("I am here and meth name is", meth_name)
        #if meth_name in self.reachable_methods: return
        #print("And we passed over the return")
        self.func_name = node.name
        if hasattr(node,"returns") and node.returns != None and ast.unparse(node.returns) != "None":
           #print("Here adding return: ", node.name, ast.unparse(node.returns))
           self._add_to_map(self.func_name+"_ret","ANNO:"+ast.unparse(node.returns))
        self.generic_visit(node)
        self.func_name = None

    def visit_AsyncFunctionDef(self,node):
       self._add_to_map(node.name+"_ret","coroutine",asynch=True)
       self.visit_FunctionDef(node)
          
def infer(package_dir,package_name,key_to_pt_type):

    reachable_methods = []
    type_map = {}
    # Step 1. get reachable methods (from key_to_pt_table) in a list
    for key in key_to_pt_type:
        index = key.rfind("\', \'")
        #print("HERE in reachable methods search")
        #print(key, key_to_pt_type[key],index)
        meth_name = key[:index+1]+")"
        #print("And meth name is",meth_name)
        if meth_name not in reachable_methods: reachable_methods.append(meth_name)
            
    # Step 2. run visitor on the pacakge dir and collect additional type info in visitor.type_map    
    for path, directory, files in os.walk(package_dir):
     for file in files:
      if file.endswith(".py"):
        file_name = os.path.join(path, file).replace("\\","/").replace("C:","") # remove "C:" to avoid split() issue
        if "/tests/" in file_name: continue # Skipping analysis of test files
        if "/test/" in file_name: continue # Skipping analysis of test files
        #if "base.py" not in file_name: continue 
        abbrev_file_name = file_name[len(package_dir):]
        #print("Processing file: ",file_name)
        infer_visitor = ShallowInferVisitor(abbrev_file_name,package_name,reachable_methods,type_map)
        try:
          with open(file_name, "r") as source:   
            tree = ast.parse(source.read(), type_comments=True, feature_version=sys.version_info[1])
            infer_visitor.visit(tree)
        except SyntaxError:
          #print("Oops, Syntax error: ")
          ...
        #print("Done processing: ",file_name)
       
    # Step 3. write type map into key_to_pt_type
    #print("Writing type_map: ") 
    #key_to_pt_type += type_map   
    for key in type_map:
       #print(key, type_map[key])    
       # key_to_pt_type[key] = str(type_map[key])       
       if key in key_to_pt_type:
          for new_type in type_map[key]:
             if new_type not in key_to_pt_type[key]: key_to_pt_type[key].append(new_type)
       else:
          key_to_pt_type[key] = type_map[key]
