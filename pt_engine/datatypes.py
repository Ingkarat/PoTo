import ast

import pt_engine.globals as globals
from .utils.base import ins 
#import pt_engine.worklist as worklist
#import pt_engine.visitors.function_visitor as function_visitor
from .visitors.function_visitor import add_function_rep

class Object:

    '''
    Attributes
    ----------

    kind : ['user','proto','meta_cls','meta_func','list_builtin','tuple_builtin','dict_builtin']
    func : optional ast.FunctionDef (Rep invariant: kind == meta_func => func != None)
    cls : optional ast.ClassDef (Rep invariant: kind == meta_cls => cls != None)
    prototype : A Python-created object (when kind is proto)
    cls_meta_obj : optional ast.ClassDef (when kind is user)
    module_name : str; name of module that defines Object when Object is either meta_func or meta_cls; name of module that creates Object otherwise
    '''

    def __init__(
            self,
            kind,
            func=None,
            cls=None,
            cls_meta_obj=None,
            closure_bindings = None,
            module_name=None,
            prototype=None
    ):
        self.kind = kind
        self.func=func
        self.cls=cls
        self.cls_meta_obj=cls_meta_obj # user object only
        self.closure_bindings = closure_bindings # func object only
        self.module_name=module_name
        self.prototype=prototype
    
    def pretty_print(self):
        if self.kind == 'meta_cls':
            print("meta_cls", self.module_name, self.cls.name)
        elif self.kind == 'meta_func':
            print("meta_func", self.module_name, self.func.name, self.closure_bindings)
        elif self.kind == 'user':
            print("user", self.module_name)
            self.cls_meta_obj.pretty_print()
        elif self.kind == 'proto':
            print("proto", self.prototype)
        elif self.kind == 'tuple_builtin' or self.kind == 'list_builtin' or self.kind == 'dict_builtin':
            print(self.kind, self.module_name)
        else:
            print("Unknonwn object:", self.kind)

class Module:
    '''
    Attributes
    ----------

    path : str
    classes : List[ast.ClassDef]
    funcs : List[ast.FunctionDef]
    module_initializer : ast.FunctionDef
    extern_env : List[ast.Import]
    package_env : List[ast.Import]
    '''

    def __init__(
            self,
            path
    ):
        self.path = path
        self.classes = [] 
        self.funcs = []
        self.module_initializer = None # set of statements (initializers) in module context
        self.module_init_body = None
        self.extern_env = []
        self.package_env = []

    # requires classDef notin self.classes    
    def add_classDef(self,classDef):
        self.classes.append(classDef)
        
    # requires functionDef notin self.funcs
    def add_funcDef(self,functionDef):
        self.funcs.append(functionDef)    

    def add_extern_env(self,import_node):
        self.extern_env.append(import_node)

    def add_package_env(self,import_node):
        self.package_env.append(import_node)

    def pretty_print(self):
        print("--- Printing Module ---")
        print("Path: ",self.path)
        print("Classes: ")
        for cls in self.classes:
            print("----", cls.name)
        print("Funcs: ")
        for func in self.funcs:
            print("----",func.name)
        print("Module initializer: pass")
        print("External imports: ")
        for imp in self.extern_env:
            print("----", ast.unparse(imp))
        print("Package imports: ")
        for imp	in self.package_env:
            print("----", ast.unparse(imp))

    # Searches for name in this Module
    def search_name(self,name,level=0):
        # name is the id of Name node
        # print("!!!Searching",self.path,"for name",name, "at level =",level)
        
        if self.module_initializer not in globals.local_env:
            if globals.package_name == "ansible":
                assert False
            module_name = globals.module_names[self.module_initializer]
            module_obj = globals.package_env[module_name]
            add_function_rep(module_obj,module_name,self.module_initializer,[])
            # Now add_function_rep for all class initializers too 
            # TODO: Test class initializers!
            self.load_class_initializers(module_obj,module_name)

        for cls in self.classes:
            if cls.name == name:
                #print("FOUND class ",name)
                return [(self.path+":"+cls.name, cls)]
        for func in self.funcs:
            if func.name == name:
                #print("FOUND fun ",name)
                return [(self.path+":"+func.name, func)]
        # Now searching in module environment for module-level vars 
        # Since the module initializer is analyzed like a regular function def, it's environemnt is saved in globals.local_env
        '''
        if self.module_initializer not in globals.local_env:
            module_name = globals.module_names[self.module_initializer]
            module_obj = globals.package_env[module_name]
            add_function_rep(module_obj,module_name,self.module_initializer,[])
            # Now add_function_rep for all class initializers too 
            # TODO: Test class initializers!
            self.load_class_initializers(module_obj,module_name)
        '''    
        for var in globals.local_env[self.module_initializer]:
            if var == name:
                # if "registry" in name: print("!!!Found it",globals.local_env[self.module_initializer][var])
                return [(self.path+":"+"module_initializer", globals.local_env[self.module_initializer][var])]  
        if level == 2: return [] # Search in next module file
        # Otherwise, look into local imports
        result = []
        name_to_search = None
        module_name = None
        for imp in self.package_env:
            if not ins(imp,ast.ImportFrom): continue
            # module_name = imp.module
            for alias in imp.names:
                if alias.name == name:
                    name_to_search = name
                    break
                if alias.asname != None and alias.asname == name:
                    name_to_search = alias.name
                    break
            if name_to_search != None: # i.e., we found a name
                module_name = imp.module
                break       
        if module_name == None: return [] # We did not find the name in import declararions, returning     
        #print("Name_to_search:", name_to_search, "for name", name, "and module name: ", module_name)         
        for pack_name in globals.package_env:
            # TODO: Needs a fix. Properly account for relative imports. Remove the None check.
            # Return an optional Node, not a list.
            #print("Trying to find name in pacakge before...",pack_name,module_name)
            if module_name in pack_name.replace('/','.'):
                #print("Partial success trying to find ", module_name, " in package ", pack_name)
                extension = globals.package_env[pack_name].search_name(name_to_search, level=level+1)
                for tup in extension:
                    if tup not in result: result.append(tup)
                # result = result + globals.package_env[pack_name].search_name(name, level=level+1)
        #print("!!!Searching",self.path,"for name",name, "at level =",level)
        return result

    # Searches for attribute-qualified name in this Module
    def search_attribute(self, attr_value, attr_str):
        #if "error" in attr_value: print("!!!!Searching attribute: ", attr_value, attr_str)
        result = []
        module_to_search = None
        for imp in self.package_env:
            for alias in imp.names:
                #if "error" in attr_value: print("!!!!Searching attribute, alias: ", ast.unparse(imp), attr_value, attr_str)
                if alias.name == attr_value:
                    module_to_search = attr_value
                    break
                if alias.asname != None and alias.asname == attr_value:
                    module_to_search = alias.name
                    break
            if module_to_search != None: # i.e., we found a package
                break 
        if module_to_search == None: 
            return result # This is not a package ref. This is a local ref.     
        # print("Package_to_search:", module_to_search, "and name to search: ", attr_str)         
        for pack_name in globals.package_env:
            # print("current package name: ", pack_name, pack_name.replace('/','.'))
            if module_to_search in pack_name.replace('/','.'):
                #print("Trying to find name in package: ", pack_name)
                extension = globals.package_env[pack_name].search_name(attr_str, level=1)
                for tup in extension:
                    if tup not in result: result.append(tup)
                #result = result + globals.package_env[pack_name].search_name(attr_str, level=1)
        return result
    
    # adds all class initializers when module is seen
    def load_class_initializers(self,module_obj,module_name):
        assert module_obj == self
        for class_def in module_obj.classes:
            class_init_body = []
            for elem in class_def.body:
                if ins(elem,ast.Assign) or ins(elem,ast.For):
                    class_init_body.append(elem)
            if class_init_body != []:        
                arguments = ast.arguments(posonlyargs=[],args=[],kwonlyargs=[],kw_defaults=[],defaults=[])
                class_initializer = ast.FunctionDef(name=class_def.name+"_class_initializer",args=arguments,body=class_init_body) 
                globals.module_names[class_initializer] = module_name
                add_function_rep(module_obj,module_name,class_initializer,[])
                globals.class_initializers[class_def] = class_initializer
               
                pp = self.path
                #s = pp.replace("/Users/ingkarat/Documents/GitHub/AIML-Proposal/pt_analysis/orig_pro_dynamic/cerberus/", "")
                #s = s.replace("/Users/ingkarat/Documents/GitHub/AIML-Proposal/pt_analysis/orig_pro_dynamic/pygal/", "")
                #s = s.replace("/Users/ingkarat/Documents/GitHub/AIML-Proposal/pt_analysis/orig_pro_dynamic/mtgjson/", "")
                #s = s.replace("/Users/ingkarat/Documents/GitHub/AIML-Proposal/pt_analysis/orig_pro_dynamic/sc2/", "")
                #s = s.replace("/Users/ingkarat/Documents/GitHub/AIML-Proposal/pt_analysis/orig_pro_dynamic/zfsp/", "")
                #s = s.replace("/Users/ingkarat/Documents/GitHub/AIML-Proposal/pt_analysis/orig_pro_dynamic/invoke/", "")
                s = pp.replace(globals.curr_package_dir, "")
                s = s + ":" + class_def.name
                #print(s)
                if class_initializer not in globals.encl_path:
                    globals.encl_path[class_initializer] = s
                else:
                    assert globals.encl_path[class_initializer] == s
                #assert False