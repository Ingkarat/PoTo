import ast
import pickle
import sys
import os
import pathlib
import time
import warnings
warnings.filterwarnings("ignore") # To suppress warning from concrete evaluation attempts (i.e. exec(...)). (Not really working !?)

sys.path.insert(1, sys.path[0]+'/pt_engine')

from pt_engine.worklist import main as wl_main
import pt_engine.globals as globals

def main(argv):

    # TODO: edit package_name and current_dir 
    package_name = "cerberus"
    current_dir = ".../PoTo/"
    base_path_to_DLInfer_package = current_dir + "orig_pro_dynamic/"
    package_dir = base_path_to_DLInfer_package + package_name + "/"
    
    # This one triggers an exit from dynamic evaluation, need to skip?
    # Running  tests/unit/bokeh/application/handlers/test___init___handlers.py [73 of 280 files] 

    d = {
        "cerberus": "cerberus/cerberus/tests/",
        "pygal": "pygal/pygal/test/",
        "zfsp": "zfsp/tests/",
        "sc2": "sc2/test/",
        "mtgjson": "mtgjson/tests/",
        "invoke": "invoke/tests/",
        "bokeh": "bokeh/tests/",
        "wemake_python_styleguide": "wemake_python_styleguide/tests/",
        "anaconda": "anaconda/test/",
        "ansible": "ansible/test/",
    }
    # directory storing test files
    test_dir = base_path_to_DLInfer_package + d[package_name]

    start = time.time()

    # 1. To run one specific test
    #run_one(package_dir, package_name, test_dir, func_name, file_name, current_dir)

    # 2. To run all test functions in a file
    # run_all_in_a_file(package_dir, package_name, test_dir, file_name, current_dir)

    # 2.5. To run all test functions in a file, without resetting global state
    # run_all_in_a_file_at_once(package_dir, package_name, test_dir, file_name, current_dir, True)

    # 3. To run all tests in "test_dir"
    run_all_tests_in_package(package_dir, package_name, test_dir, current_dir)

    # 4. To merge result into "merged_PACKAGENAME_no_tests.pkl" file
    merge_result_without_tests_file(package_name, current_dir)

    end = time.time()
    print(end - start, "seconds")
    print("=== END poto.py ===")

def get_pkl_name(test_dir, func_name, file_name):
    x = file_name.replace(test_dir, "")
    x = x.replace("/","__")
    return "(" + x + ")" + func_name + ".pkl"

def run_one(package_dir, package_name, test_dir, func_name, file_name, current_dir):
    #print(package_dir, package_name, test_dir, func_name, file_name)
    globals.reset_globals()
    globals.package_name = package_name
    globals.curr_package_dir = package_dir
    globals.main_name = func_name
    globals.write_pkl_name = get_pkl_name(test_dir, func_name, file_name)
    w_path = current_dir + "poto_result/" + package_name + "/"
    globals.write_pkl_base = w_path
    if not os.path.exists(w_path):
        os.makedirs(w_path)
    wl_main(file_name, func_name, package_dir, package_name, True)

def get_func_list_from_file(file_name):
    ll = []
    class FuncLister(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            ll.append(node.name)
            #self.generic_visit(node)  we want only top-level functions
        def visit_AsyncFunctionDef(self, node):
            ll.append(node.name)
            #self.generic_visit(node)  we want only top-level functions

    with open(file_name, "r") as source:
        tree = ast.parse(source.read(), type_comments=True, feature_version=sys.version_info[1])
        FuncLister().visit(tree)

    return ll

def run_all_in_a_file(package_dir, package_name, test_dir, file_name, current_dir):
    ll = get_func_list_from_file(file_name)
    for l in ll:
        run_one(package_dir, package_name, test_dir, l, file_name, current_dir)

def run_all_in_a_file_at_once(package_dir, package_name, test_dir, file_name, current_dir, run_initializers):
    #print("\n\n\nIN AT ONCE:", package_dir, package_name, test_dir, file_name, file_name)
    globals.write_pkl_name = get_pkl_name(test_dir, "_ALL_FUNCS_", file_name)
    w_path = current_dir + "poto_result/" + package_name + "/"
    globals.write_pkl_base = w_path
    #globals.write_pkl_name = get_pkl_name(test_dir, "_ALL_FUNCS_", file_name)
    #globals.write_pkl_base = current_dir + package_name + "/"
    wl_main(file_name, None, package_dir, package_name,run_initializers, all_funcs = True)

def get_all_py_in_dir_full_path(test_dir):
    p = test_dir
    pl = pathlib.Path(p)
    gl = pl.rglob("*")
    l = []
    for posix_path in gl:
        if posix_path.is_file():
            f = str(posix_path)
            if f.endswith(".py"):
                l.append(f)
    return l

def run_all_tests_in_package(package_dir, package_name, test_dir, current_dir):
    globals.curr_package_dir = package_dir
    ll = get_all_py_in_dir_full_path(test_dir)
    ll.sort()  
    #error_lists = ["/bokeh/tests/__init__.py"]
    error_lists = []

    not_ok = []
    def is_ok(l):
        for el in error_lists:
            if el in l: return False
        return True

    analyze = True
    i = 0
    for l in ll:
        i += 1
        file_name = l

        if ".py~" in file_name: continue
        if not file_name.endswith(".py"): continue
        
        if analyze == False: continue
        
        globals.curr_package_dir = package_dir
        print("Running ", shorten(l), "[{} of {} files]".format(i, len(ll)))
        # if i <= 75: continue #TODO: bokeh 75 kicks out evaluation; uncomment this to continue running tests
        if not is_ok(l):
            not_ok.append(l)
            continue
        run_initializers = True if i == 1 else False
        run_all_in_a_file_at_once(package_dir, package_name, test_dir, file_name, current_dir, run_initializers) 
    print("Finished running {} files in {}".format(len(ll), shorten(test_dir)))
    if True:
        print("not_ok")
        for no in not_ok:
            print(no)
    #print("\n\n", text)
    #print("\n",fail_text)
    #print("\n num_file =", len(ll), "[pass/fail] =", pp, ff)

def shorten(p):
    if p is None: return p
    p = p.replace(globals.curr_package_dir, "")
    return p

def get_pkl_files(package_name, current_dir):
    base = current_dir + "poto_result/" + package_name + "/"
    l = []
    for f in os.listdir(base):
        if ".pkl" in f:
            l.append(base + f)
    return l

def merge_result_without_tests_file(package_name, current_dir):
    ll = get_pkl_files(package_name, current_dir)
    dd = {}
    for l in ll:
        with open(l, 'rb') as f:
            d = pickle.load(f)

            for k in d.keys():
                (aa,bb,cc) = k
                k1 = (aa,bb,cc)

                #print("\nk =",k, k[0])
                #print("\t", d[k])

                if "/tests/" in k[0]: # We exclude those in /tests/ files
                    continue
                if "/test/" in k[0]: # We exclude those in /test/ files
                    continue
                if "/test_PT/" in k[0]: # We exclude /test_PT/ files too
                    continue
                if "/typeshed_builtins/" in k[0]: # Now we exclude this too
                    continue
                
                if k1 not in dd:
                    dd[k1] = d[k]
                else:
                    tt = d[k]
                    for t in tt:
                        if t not in dd[k1]:
                            oo = dd[k1]
                            oo.append(t)
                            dd[k1] = oo

    if False:
        print("\n\nMERGED DICT")
        for l in ll:
            print("func:", l)
        for k in dd.keys():
            print("\n", k)
            print("\t", dd[k]) 
    
    path = current_dir + "poto_result/" + "merged_poto_" + package_name + ".pkl"
    with open(path, 'wb') as f:
        pickle.dump(dd, f, protocol=pickle.HIGHEST_PROTOCOL)  


if __name__ == "__main__":
    main(sys.argv[1:])
    #print("=== END ===")
