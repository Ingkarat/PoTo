import ast

import pt_engine.globals as globals
from ..datatypes import Module

def print_map(the_map):
  print("\n\n Printing the map\n")
  for key in the_map.keys():
    print("A key: ", key)
    for val in the_map[key]:
      print("---- A value: ",val)
  print("Size of the map: ",len(the_map.keys()))

def print_simple_map(the_map):
  print("\n\n Printing the simple map, keys only:")
  for key in the_map.keys():
    print("A key: ", key)


class ClassFuncInnerVisitor(ast.NodeVisitor):
  def __init__(self, e_path):
    self.e_path = e_path # encl_path of this node (eg. .../main.py:cls)
    self.path = [] # current path

  def path_to_str(self):
    s = self.e_path
    for p in self.path:
      s = s + "." + p
    return s.replace(":.",":") 

  def visit_ClassDef(self, node):
    self.path.append(node.name)
    self.generic_visit(node)
    self.path.pop()

  def visit_FunctionDef(self, node):
    self.path.append(node.name)
    s = self.path_to_str()
    if node not in globals.encl_path:
      globals.encl_path[node] = s
    else:
      assert globals.encl_path[node] == s
    self.generic_visit(node)
    self.path.pop()

  def visit_AsyncFunctionDef(self, node):
    self.path.append(node.name)
    s = self.path_to_str()
    if node not in globals.encl_path:
      globals.encl_path[node] = s
    else:
      assert globals.encl_path[node] == s
    self.generic_visit(node)
    self.path.pop()

class ModuleVisitor(ast.NodeVisitor):
    def __init__(self,file_name,package_name):
      self.module_name = file_name
      self.package_name = package_name
      self.module_obj = Module(file_name)
      self.module_init_body = []
      self.import_list = []

    def visit_Import(self, node):
      #print("Visiting import: ",ast.unparse(node)," and ast dump: ",ast.dump(node))
      # TODO: What if some names are extern imports and other are package ones
      # TODO: Right now we assume all are either extern or package
      for alias in node.names:
        self.import_list.append(alias.name)
        if self.package_name in ast.unparse(alias):
          # Add it as internal import
          self.module_obj.add_package_env(node)
          return
      self.module_obj.add_extern_env(node)
      
    def visit_ImportFrom(self, node):
      if node.level == 0 and self.package_name not in node.module:
        self.import_list.append(node.module)
        # Adding an external import
        self.module_obj.add_extern_env(node)
      else:
        self.module_obj.add_package_env(node)

    def visit_ClassDef(self, node):
      self.module_obj.add_classDef(node)
      globals.module_names[node] = self.module_name
      cfiv = ClassFuncInnerVisitor(self.module_name+":")
      cfiv.visit(node)

    def visit_FunctionDef(self, node):
      self.module_obj.add_funcDef(node)
      globals.module_names[node] = self.module_name
      cfiv = ClassFuncInnerVisitor(self.module_name+":")
      cfiv.visit(node)

    def visit_AsyncFunctionDef(self, node):
      self.module_obj.add_funcDef(node)
      globals.module_names[node] = self.module_name
      cfiv = ClassFuncInnerVisitor(self.module_name+":")
      cfiv.visit(node)

    #def visit_If(self, node):
    #  self.module_init_body.append(node)
    def visit_For(self, node):
      self.module_init_body.append(node)
    def visit_Assign(self,node):
      #print("HERE visiting assign in module...",ast.unparse(node))
      self.module_init_body.append(node)
    def visit_AnnAssign(self,node):
      self.module_init_body.append(node)
    def visit_AugAssign(self,node):
      self.module_init_body.append(node)

    # requires: runs after ModuleVisitor.visit          
    def post_process(self): 
      # Now form module_initializer function
      # Will create rep lazily, only if needed during constraint resolution
      self.module_obj.module_init_body = self.module_init_body
      arguments = ast.arguments(posonlyargs=[],args=[],kwonlyargs=[],kw_defaults=[],defaults=[])
      module_initializer = ast.FunctionDef(name="module_initializer",args=arguments,body=self.module_init_body) 
      self.module_obj.module_initializer = module_initializer
      globals.module_names[module_initializer] = self.module_name
      globals.entry_points.append(module_initializer)
      # If module is the typeshed module, initialize accordingly
      # Otherwise, add the initializers to the entry points
      if 'typeshed_builtins' in self.module_name:
        globals.typeshed_builtins_module = self.module_obj
      pp = self.module_name
      s = pp.replace(globals.curr_package_dir, "")
      #print(s)
      if module_initializer not in globals.encl_path:
        globals.encl_path[module_initializer] = s
      else:
        assert globals.encl_path[module_initializer] == s
          