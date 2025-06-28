import ast
import os
import sys

import pt_engine.globals as globals

from pt_engine.visitors.module_visitor import ModuleVisitor
from pt_engine.visitors.function_visitor import add_function_rep
from pt_engine.utils.base import ins

# Worklist maintains a set of functions to analyze
worklist = []

# Crawls through package directory and creates a "package_env" map: Full_file_path -> Module object.
# A Module object contains info of directly enclosing classes and funcs
def init_package_env(package_dir, package_name):
  list_of_import = []
  for path, directories, files in os.walk(package_dir):
    for file in files:
      if file.endswith(".py"):
        file_name = os.path.join(path, file).replace("\\","/").replace("C:","") # remove "C:" to avoid split() issue
        if "/tests/" in file_name: continue # Skipping analysis of test files
        if "/test/" in file_name: continue # Skipping analysis of test files
        #print("Analyzing: ",file_name
        module_visitor = ModuleVisitor(file_name,package_name)
        try: 
          with open(file_name, "r") as source:
            tree = ast.parse(source.read(), type_comments=True, feature_version=sys.version_info[1])
            module_visitor.visit(tree)
            module_visitor.post_process()
        except SyntaxError:
          print("Oops, Syntax error: ")
        except UnicodeDecodeError:
          print("Rare case in some files. Skip them.")
        for im in module_visitor.import_list:
         if im not in list_of_import:
            list_of_import.append(im)
        #print("Done analyzing: ",file_name)
        #module_visitor.module_obj.pretty_print()
        globals.package_env[file_name] = module_visitor.module_obj
  
# Initializes class hierarchy:
# superclasses[cls] collects the base classes in order they appear
def init_class_hierarchy():
   for module in globals.package_env:
      module_obj = globals.package_env[module]
      for cls in module_obj.classes:
         globals.superclasses[cls] = []
         for base in cls.bases:
            if not (ins(base,ast.Name) or ins(base,ast.Attribute)): continue #TODO: revisit. 
            base_class_defs = ""
            if ins(base,ast.Name):
                base_class_defs = module_obj.search_name(ast.unparse(base))
            elif ins(base,ast.Attribute):
                base_class_defs = module_obj.search_attribute(ast.unparse(base.value),base.attr)
            for base_cls in base_class_defs:
               #assert ins(base_cls[1],ast.ClassDef), "Not a class def: "+base_cls[0]+','+base_cls[1]
               if ins(base_cls[1],ast.ClassDef) and base_cls[1] not in globals.superclasses[cls]:
                  globals.superclasses[cls].append(base_cls[1])        

# properties[cls] collects property getters and setters: {'prop_name' : {'getter':functionDef, 'setter':functionDef}}
def init_properties():
   for module in globals.package_env:
      module_obj = globals.package_env[module]
      for cls in module_obj.classes:
         globals.properties[cls] = {}
         for elem in cls.body:
            if ins(elem,ast.FunctionDef) or ins(elem,ast.AsyncFunctionDef):
               if elem.decorator_list == None:
                  continue
               for decorator in elem.decorator_list:
                  if ins(decorator,ast.Name) and decorator.id == 'property':
                     globals.properties[cls] = {elem.name:{}}
                     globals.properties[cls][elem.name]['getter'] = elem
                  elif ins(decorator,ast.Attribute) and (decorator.attr == 'getter' or decorator.attr == 'setter'): # This is a property setter or getter
                     #Assumes property has been "declared" ahead of it's setters and getters
                     dec_kind = decorator.attr
                     prop_name = decorator.value.id 
                     #print("ADDING a property:",dec_kind,prop_name)
                     globals.properties[cls][prop_name][dec_kind] = elem   

# Computes the MRO of each class
# TODO: Dylan algorithm from Barret et al. OOPSLA'96; Have to switch to C3 
def init_mros():
   def mro(cls):
      def filter_out(c, list):
         result = []
         for elem in list:
            if elem != c: result.append(elem)
         return result
      
      # TODO: Need to change to C3, this is Dylan's original algorithm 
      def candidate(c,remaining_inputs):
         def head(lis):
            if len(lis) > 0 and c == lis[0]: return c
            return None
         def tail(lis):
            if len(lis) > 0 and c in lis[1:]: return c
            return None
         head_flag = False
         for input_seq in remaining_inputs:
            if head(input_seq): head_flag = True 
         tail_flag = False
         for input_seq in remaining_inputs:
            if tail(input_seq): tail_flag = True
         if head_flag and not tail_flag: return c   
         return None
      
      def candidate_direct_superclass(c,remaining_inputs):
         for super in globals.superclasses[c]:
            if candidate(super,remaining_inputs) != None:
                return super
         return None

      def merge_lists(partial_result,remaining_inputs):
         empty_flag = True
         for seq in remaining_inputs:
            if seq != []: empty_flag = False
         if empty_flag:
            return list(reversed(partial_result))
         else:   
            next = None
            for elem in partial_result:
               cand = candidate_direct_superclass(elem,remaining_inputs) 
               if cand != None:
                  next = cand
                  break
            if next != None:
               new_remaining_inputs = []
               for seq in remaining_inputs:
                  new_remaining_inputs.append(filter_out(next,seq))
               return merge_lists([next]+partial_result,new_remaining_inputs)
            else:
               assert False, "Inconsistent MRO!"+cls.name 

      if cls in globals.mros: return globals.mros[cls]
      sups_mros = []
      sups = []

      zfsp_RecurssionError = ast.ClassDef(name='Struct', bases=[ast.Name(id='Struct', ctx=ast.Load())], keywords=[ast.keyword(arg='metaclass', value=ast.Name(id='StructMeta', ctx=ast.Load()))], body=[ast.Pass()], decorator_list=[])

      for super in globals.superclasses[cls]:
         #for zfsp
         if 1:
            # 100% disaster will happen here but should be fine if checking just this one ClassDef
            if ast.dump(super) == ast.dump(zfsp_RecurssionError):
               continue
         sups_mros.append(mro(super))
         sups.append(super) 
      sups_mros.append(sups)
      result = merge_lists([cls],sups_mros)
      globals.mros[cls] = result
      assert result != None, "none for "+cls.name
      return result
   for cls in globals.superclasses:
      cls_mro = mro(cls)
      globals.mros[cls] = cls_mro
      #print("\n Printing the mro of",cls.name)
      #for linear in cls_mro:
      #  print(linear.name)

def add_to_worklist(func_def):
    if func_def not in worklist:
        worklist.append(func_def)

def add_module_initializers_to_worklist(run_initializers):
   #if globals.local_env != {}: return # Don't analyze again if next package
   # Runs initializers once to speed up larger benchmarks
   if run_initializers == False: return 
   for initializer in globals.entry_points:
      if initializer not in globals.local_env: # initializer not in global environment yet
         print("OFFENDING NAME ",globals.module_names[initializer],len(globals.module_names[initializer]))
         module_name = globals.module_names[initializer]
         module_obj = globals.package_env[module_name]
         add_function_rep(module_obj,module_name,initializer,[])
         # Now add_function_rep for all class initializers too 
         # TODO: Test class initializers!
         module_obj.load_class_initializers(module_obj,module_name) 
      
      add_to_worklist(initializer)       
   for class_def in globals.class_initializers:
      add_to_worklist(globals.class_initializers[class_def])       

def add_main_to_worklist(main_module_name,main_func_name,package_name,all_funcs = False):      
    if main_module_name.endswith(".py"):
        #print("(add_main_to_) Analyzing: ",main_module_name);
        main_module_visitor = ModuleVisitor(main_module_name,package_name)
        try: 
          with open(main_module_name, "r") as source:
            tree = ast.parse(source.read(), type_comments=True, feature_version=sys.version_info[1])
            main_module_visitor.visit(tree)
            main_module_visitor.post_process()
        except SyntaxError:
          print("Oops, Syntax error: ")
        #print("(add_main_to_) Done analyzing: ",main_module_name, len(main_module_name))
        globals.package_env[main_module_name] = main_module_visitor.module_obj

        #main_module_visitor.module_obj.pretty_print()
        #assert False 

        for func in main_module_visitor.module_obj.funcs:
            #print(">> ", func.name)
            if all_funcs or func.name == main_func_name: #"main":
                main_def = func 
                # [] assumes main has no formal parameters
                add_function_rep(main_module_visitor.module_obj,main_module_visitor.module_name,main_def,[])
                add_to_worklist(main_def)
                globals.encl_path[main_def] = main_module_name + ":" + main_def.name

def worklist_solve(run_initializers):
    global worklist
    while len(worklist) > 0:
        next_func_def = worklist[0]
        #print("Next function def: ", next_func_def.name)
        #print("Removed from wl: ",next_func_def.name, globals.module_names[next_func_def])
        worklist = worklist[1:] # remove first elem
        change = []
        if next_func_def not in globals.stmts: continue
        # Runs run_initializers == False runs analysis once to speed up larger benchmarks. No impact on precision
        if run_initializers == False: 
           if "module_initializer" == next_func_def.name: continue 
        for stmt in globals.stmts[next_func_def]:
            #stmt.pretty_print()
            # solve returns list of functions that may be affected; list pushed back to wl
            change_stmt = stmt.solve()
            for func in change_stmt:
               if func not in change: change.append(func)
        for func in change:
            add_to_worklist(func)
    #globals.print_globals() 
    

def main(main_module,main_func,package_dir,package_name,run_initializers,all_funcs = False):
  init_package_env(package_dir,package_name)
  #print("\n= FINISHED init_package_env() =\n")
  #print(globals.print_globals())
    
  add_main_to_worklist(main_module,main_func,package_name,all_funcs)
  #print("\n= FINISHED add_main_to_worklist() =\n")

  add_module_initializers_to_worklist(run_initializers)
  #print("\n= FINISHED add_module_initializers to worklist") 

  init_class_hierarchy()
  #print("\n= FINISHED init_class_hierarchy() =\n")

  init_mros()
  #print("\n= FINISHED init_mros() =\n")
  init_properties()
  #print("\n= FINISHED init_properties() =\n")

  worklist_solve(run_initializers)
  #print("\n= FINISHED worklist_solve() =\n")

  #globals.cg_nodes_to_pkl()
  globals.process_types(printing = False) # print T/F
  
  #print("=== DONE (worklist.main()) ===")
  #globals.call_graph.printGraph(globals.encl_class)
  #globals.call_graph.cg_to_pkl(globals.encl_class) # PROBABLY WHERE WE WRITE CG. DOUBLE CHECK
  globals.get_more_callgraph_info_from_ptgraph(printing = False) # MAYBE we dont need the above becuase this is the better version
  globals.reset_globals() 
      

if __name__ == "__main__":
  main_module = sys.argv[1]
  main_func = sys.argv[2]
  package_dir = sys.argv[3]
  package_name = sys.argv[4]
  main(main_module,main_func,package_dir,package_name)
  print("DONE")
