import ast
import sys

import pt_engine.globals as globals

def ins(obj,cls):
    return isinstance(obj,cls)

def ins(obj,cls):
  return isinstance(obj,cls)

def obj_to_list(obj,list):
  if obj not in list: list.append(obj)

def list_to_list(list1,list2):
  for obj in list1:
    if obj not in list2: list2.append(obj)

def is_stmt(node):
   stmt_list = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Return, ast.Delete)
   stmt_list += (ast.AnnAssign, ast.Assign, ast.AugAssign)
   stmt_list += (ast.For,ast.AsyncFor,ast.While,ast.With,ast.AsyncWith,ast.If)
   stmt_list += (ast.Raise,ast.Try,ast.Assert,ast.Import,ast.ImportFrom,ast.Global,ast.Nonlocal,ast.Expr,ast.Pass,ast.Break,ast.Continue)
   return isinstance(node,stmt_list)

def eval_with_return_in_extern(node,extern_env,locals={}): 
  exec_str = ""
  # TODO: In one bench, invoke, execution closed STDOUT
  if "os.path.splitext" in node: return "None_Found" # print("OFFENDING: ", node)
  if "self." in node: return "None_Found" # print("OFFENDING: ", node)
  if "read" in node: return "None_Found"
  if "close" in node: return "None_Found"
  if "sleep" in node: return "None_Found"
  if "exit" in node: return "None_Found"
  if "write" in node: return "None_Found"
  if "vars" in node: return "None_Found"
  if "" == node: return "None_Found"
  #print("OFFENDING EVAL:",node)
  #if node == "": return "None_Found"
  #print("And now here", node)
  #if "re.compile" in node: return "None_Found"
  #print("And now here 3", type(node),node == "")
  for extern_imp in extern_env:
    add = True
    #print(ast.unparse(extern_imp))
    try:
       exec(ast.unparse(extern_imp))
    except (ModuleNotFoundError,ImportError,TypeError):
       #print("UUUUUUUUUUUUUUUUUUU")
       add = False # remove that import from eval env  
    exec_str += ast.unparse(extern_imp)+ "; " if add else ""
  #print("And... exec_str so far",exec_str)
  exec_str += "ret_val="+node #ast.unparse(node)                                                                                                                            
  try:
    #locals = {}
    exec(exec_str,None,locals)
  except:
    #print("\n",exec_str, "IS NOT PART of extern invironment, try resolving in package env (eval_with_return_in_extern)")
    return "None_Found" 
  #print(node, locals['ret_val'], "IS PART of extern env, but not a constant (eval_with_return_in_extern)")
  #print(exec_str, "|", locals['ret_val'])
  return locals['ret_val']

def is_universal_constant(proto_obj):
   return isinstance(proto_obj,(str,int,float,complex,bool,bytes))

def is_proto_container(obj,containers=("<class 'dict'>","<class 'list'>","<class 'tuple'>")):
    result = False
    if obj.kind == 'proto':
        locals = {'obj':obj}
        try:
          exec('type_of = type(obj.prototype)',None,locals)
        except:
          ...
        type_of = locals['type_of']
        if str(type_of) in containers:
            result = True
    return result

# requires: proto_obj is a prototype, i.e., concrete value, not an abstract object
def cast_proto_container(proto_obj):
    locals = {'proto_obj':proto_obj}
    try:
      exec('type_of = type(proto_obj)',None,locals)
    except:
      ...
    if str(locals['type_of']) in ("<class 'dict_items'>","<class 'dict_values'>","<class 'dict_keys'>","<class 'enumerate'>"): 
      locals = {'proto_obj':proto_obj}
      try:
        exec('list_value = list(proto_obj)',None,locals)
      except:
        ...
      return locals['list_value']
    else:
      return proto_obj

# const_value is node.value where node = ast.Constant(value=const_value)
def encode_constant(const_value):
  if const_value == None:
     val = "c_none_None"
  elif ins(const_value,str):
    if len(const_value)>10:
      val = "c_str_\'msg\'"
    else:
      val = "c_str_\'"+str(const_value)+"\'"
  elif ins(const_value,bool):
      val = "c_bool_"+str(const_value)
  elif ins(const_value,int):
      val = "c_int_"+str(const_value)
  elif ins(const_value,float):
      val = "c_float_"+str(const_value)
  elif ins(const_value,bytes):
      val = "c_bytes_"+str(const_value)
  elif ins(const_value,complex):
      val = "c_complex_"+str(const_value)
  else:
      #print("Offending const_value "+str(const_value)+" "+str(type(const_value)))
      val = "c_"+str(const_value)
  return val  

# Inverse of encode_constant
def decode_constant(const_value):
  if "c_none_" in const_value:
     val = None
  elif 'c_str_' in const_value:
    val = const_value[6:]
  elif 'c_int_' == const_value[:6]:
      try: 
        val = int(const_value[6:])
      except:
        val = 10 # generic integer value
  elif 'c_bool_' in const_value:
      val = bool(const_value[7:])
  elif 'c_float_' in const_value:
      val = float(const_value[8:])
  elif 'c_bytes_' in const_value:
      val = bytes(const_value[8:],encoding='utf-8')
  elif 'c_complex_' in const_value:
      val = complex(const_value[10:])
  else:
      #print("Offending const_value",const_value)
      val = const_value[2:]
  return val        

def is_constant(obj):
  return (ins(obj,str) and obj.startswith("c_"))

def maybe_to_list(val):
  return [] if val==None else val

def is_decorator(func,decorator):
    if func.decorator_list == None:
        return False
    for dec in func.decorator_list:
        #print("Next decorator!", ast.unparse(decorator))
        if ins(dec,ast.Name) and dec.id == decorator:
            return True
    return False        


class ClassVisitor(ast.NodeVisitor):
  def __init__(self, target_funcDef):
    self.target_funcDef = target_funcDef
    self.path = []
    self.ret = None

  def visit_ClassDef(self, node):
    self.path.append(node.name)
    self.generic_visit(node)
    self.path.pop()

  def visit_FunctionDef(self, node):
    self.path.append(node.name)
    if node.name == "main":
      pass
      #print(".. ", self.target_funcDef, node, self.target_funcDef.name, node.name)
    if self.target_funcDef == node:
      assert self.ret is None
      self.ret = []
      for p in self.path:
        self.ret.append(p)

    self.generic_visit(node)
    self.path.pop()

  def visit_AsyncFunctionDef(self, node):
    self.path.append(node.name)
    if node.name == "main":
      pass
      #print(".. ", self.target_funcDef, node, self.target_funcDef.name, node.name)
    if self.target_funcDef == node:
      assert self.ret is None
      self.ret = []
      for p in self.path:
        self.ret.append(p)

    self.generic_visit(node)
    self.path.pop()

def get_enclosing_class_of_f(funcDef):
  mod_names = globals.module_names[funcDef]
  class_visitor = ClassVisitor(funcDef)
  with open(mod_names, "r") as source:
    tree = ast.parse(source.read(), type_comments=True, feature_version=sys.version_info[1])
    class_visitor.visit(tree)

  class_visitor2 = ClassVisitor(funcDef)
  with open(mod_names, "r") as source:
    tree = ast.parse(source.read(), type_comments=True, feature_version=sys.version_info[1])
    class_visitor2.visit(tree)

  #print(class_visitor.ret)
  assert class_visitor.ret is not None, "Cant find the target FunctionDef. PANIC ???"

  return class_visitor.ret