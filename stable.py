"""
Reproduce numbers in the paper by using the existing result

in /stable_log/
    - all_keys_PACKAGE.pkl
    - potopus_PACKAGE.pkl
    - pytype_PACKAGE.pkl
    - DL-GT_PACKAGE.pkl
    - DL-ML_PACKAGE.pkl
    - DL-DY_PACKAGE.pkl
    - exact_partial_other.pkl = result after running the equivalence comparison.
        We have this because running is a bit expensive (O(NM)) which take about 10 minutes in total.

WIP: Figure 11 + 10 sub-figures in the Appendix
TODO: Improve these descriptions
TODO: PoToCG and PyCG (Table 3, Table 4)
TODO: Numbers for DL-ST of Anaconda are a bit off. Check why.
TODO: Numbers for Pytype of Cerberus are a bit off (after applying manual verdict). Check why/
"""

#from re import T
import sys
import pickle
import utils
from typing import List, Dict

from tabulate import tabulate, SEPARATING_LINE

def main(argv):
    current_dir = ".../ecoop_artifact_minimal_ana/"
    use_existing_exact_partial_other_pkl = True
    
    all_packages = ["cerberus", "mtgjson", "pygal", "sc2", "zfsp", 
                    "anaconda", "ansible", "bokeh", "invoke", "wemake_python_styleguide"]

    pytype_manual_verdict_ok_list = ["cerberus", "mtgjson", "pygal", "sc2", "zfsp", "wemake_python_styleguide"]

    all_keys_list = {}  # PACKAGE_NAME -> list of string.   List of "all_keys"
    all_pt_dict = {}    # PACKAGE_NAME -> PoTo+ dict.       PoTo+ dict is "string in tuple () form -> list of types"
    all_py_dict = {}    # PACKAGE_NAME -> Pytype dict.
    all_dlgt_dict = {}  # PACKAGE_NAME -> DL-GT/ST dict     
    all_dldy_dict = {}  # PACKAGE_NAME -> DL-DY dict
    all_dlml_dict = {}  # PACKAGE_NAME -> DL-ML dict

    # get "all_keys" list
    for p in all_packages:
        all_keys_list[p] = utils.get_all_keys_stable(p)

    # get "pt_dict" for each package
    for p in all_packages:
        all_pt_dict[p] = utils.get_potoplus_dict_stable(p)

    # get "pytype" for each package
    for p in all_packages:
        all_py_dict[p] = utils.get_pytype_dict_stable(p)

    # get "DL-GT/ST" for each package
    for p in all_packages:
        all_dlgt_dict[p] = utils.get_DLGT_stable(p)
    
    # get "DL-DY" for each package
    for p in all_packages:
        all_dldy_dict[p] = utils.get_DLDY_stable(p)
    
    # get "DL-ML" for each package
    for p in all_packages:
        all_dlml_dict[p] = utils.get_DLML_stable(p)
    

    # Figure 9: Coverage percentages of non-empty keys to total keys (RQ1).
    # data = all_keys, Non-empty, ratio
    present_fig9(all_packages, all_keys_list, all_pt_dict, all_py_dict, all_dlgt_dict, all_dlml_dict, all_dldy_dict)
    
    # Figure 10: Equivalence comparison between PoTo+ and other type inference techniques (RQ2).
    present_fig10_and_appendix(current_dir, pytype_manual_verdict_ok_list, all_packages, all_keys_list, all_pt_dict, all_py_dict, all_dlgt_dict, all_dlml_dict, all_dldy_dict, use_existing_exact_partial_other_pkl)

    # Table 3: Function coverage of PoToCG and PyCG (RQ5).
    present_table3(current_dir)

# Table 3: Function coverage of PoToCG and PyCG (RQ5).
def present_table3(current_dir):
    print("\nTable 3: Function coverage of PoToCG and PyCG (RQ5).")
    cg_packages = ["cerberus", "pygal", "mtgjson", "sc2", "invoke"]
    results = {}
    for p in cg_packages:
        (total_f, f_without_call, f_with_call) = utils.table3_get_total_number(p, current_dir)
        #print(p, total_f, f_without_call, f_with_call)
        r = utils.table_3_get_poto_vs_pycg(p, current_dir)
        results[p] = [total_f, f_without_call, f_with_call] + r
    hd = ["Functions", "cerberus", "pygal", "mtgjson", "sc2", "invoke"]
    row = ["Total functions", "__Funcs without a call stmt", "__Funcs with call stmt",
        "Funcs in PoToCG", "Funcs in PyCG", "Funcs in PoToCG but not in PyCG", "Funcs in PyCG but not in PoToCG", 
        "Funcs in both. Same # of edges", "__Exactly the same set of edges", "__Different set of edges", 
        "Funcs in both. #Edges: PoToCG > PyCG", "Funcs in both. #Edges: PyCG > PoToCG"]    
    data = []
    lines = [2, 6, 9]
    for i in range(12):
        l = [row[i], results["cerberus"][i], results["pygal"][i], results["mtgjson"][i], results["sc2"][i], results["invoke"][i]]
        data.append(l)
        if i in lines:
            data.append(SEPARATING_LINE)
    table = tabulate(data, headers = hd, missingval = "")
    print(table)


# Figure 9: Coverage percentages of non-empty keys to total keys (RQ1).
def present_fig9(all_packages, all_keys_list, all_pt_dict, all_py_dict, all_dlgt_dict, all_dlml_dict, all_dldy_dict):
    def f(x):
        return "{} ({:.1f}%)".format(x, (x * 100.0) / num_all_keys)
    def g(x):
        return "{:.2f}%".format((x * 100.0) / t_all_k)

    print("\nFigure 9: Coverage percentages of non-empty keys to total keys (RQ1).")
    hd = ["package", "total", "PoTo+", "Pytype", "DL-ST", "DL-ML", "DL-DY"]
    data = []
    t_all_k = t_pt = t_pyt = t_st = t_ml = t_dy = 0
    for p in all_packages:
        num_all_keys = len(all_keys_list[p])
        pt = len(utils.remove_keys_that_are_empty(all_pt_dict[p]))
        pyt = len(utils.remove_keys_that_are_empty(all_py_dict[p], is_pytype = True))
        st = len(utils.remove_keys_that_are_empty(all_dlgt_dict[p]))
        ml = len(utils.remove_keys_that_are_empty(all_dlml_dict[p]))
        dy = len(utils.remove_keys_that_are_empty(all_dldy_dict[p]))
        if p == "wemake_python_styleguide": p = "wemake"
        l = [p, num_all_keys, f(pt), f(pyt), f(st), f(ml), f(dy)]
        data.append(l)
        t_all_k += num_all_keys
        t_pt += pt
        t_pyt += pyt
        t_st += st
        t_ml += ml
        t_dy += dy
    num_pkg = len(all_packages)
    data.append(["AVERAGE", None, g(t_pt), g(t_pyt), g(t_st), g(t_ml), g(t_dy)])
    table = tabulate(data, headers = hd, missingval = "")
    print(table)

# Figure 10: Equivalence comparison between PoTo+ and other type inference techniques (RQ2).
#TODO: CURRENTLY NOT USING MANUAL VERDICT 
def present_fig10_and_appendix(current_dir, pytype_manual_verdict_ok_list, all_packages, all_keys_list, all_pt_dict, all_py_dict, all_dlgt_dict, all_dlml_dict, all_dldy_dict, use_existing_exact_partial_other_pkl = False):
    print("\nFigure 10: Equivalence comparison between PoTo+ and other type inference techniques (RQ2).")
    #TODO: reconstruct this (???)
    if not use_existing_exact_partial_other_pkl:
        dd = {}
        for p in all_packages:
            has_pytype_mv = False
            if p in pytype_manual_verdict_ok_list:
                has_pytype_mv = True
            [mv_py, mv_st, mv_dy, mv_ml] = get_manual_verdict_all_techniques(current_dir, p, has_pytype_mv)
            [py_ex, py_part, py_oth] = utils.get_exact_partial_other_pytype(all_pt_dict[p], all_py_dict[p], mv_py, p, current_dir)
            [st_ex, st_part, st_oth] = utils.get_exact_partial_other_DL(all_pt_dict[p], all_dlgt_dict[p], mv_st, p)
            [ml_ex, ml_part, ml_oth] = utils.get_exact_partial_other_DL(all_pt_dict[p], all_dlml_dict[p], mv_ml, p)
            [dy_ex, dy_part, dy_oth] = utils.get_exact_partial_other_DL(all_pt_dict[p], all_dldy_dict[p], mv_dy, p)
            #print(p, "DL-ST", st_ex, st_part, st_oth)
            d = {}
            d["py"] = (py_ex, py_part, py_oth)
            d["st"] = (st_ex, st_part, st_oth)
            d["ml"] = (ml_ex, ml_part, ml_oth)
            d["dy"] = (dy_ex, dy_part, dy_oth)
            dd[p] = d
            print(p)
            #print(p, py_ex, py_part, py_oth)
        path = current_dir + "stable_log/exact_partial_other.pkl"
        if not use_existing_exact_partial_other_pkl:
            with open(path, 'wb') as f:
                pickle.dump(dd, f, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        path = current_dir + "stable_log/exact_partial_other.pkl"
        with open(path, 'rb') as f:
            dd = pickle.load(f)
    print("\nAppendix A.1: Per-application Equivalence Comparisons including Bars for Non-Empty Variables")
    hd = ["Techniques", "PoTo+ non-empty", "tech non-empty", "mat+par+mis", "match", "partial", "mismatch"]
    t_poto = t_py = t_st = t_dy = t_ml = 0
    t_py_a = t_py_b = t_py_c = 0
    t_st_a = t_st_b = t_st_c = 0
    t_dy_a = t_dy_b = t_dy_c = 0
    t_ml_a = t_ml_b = t_ml_c = 0
    for p in all_packages:
        d = dd[p]
        data = []
        pt = len(utils.remove_keys_that_are_empty(all_pt_dict[p]))
        pyt = len(utils.remove_keys_that_are_empty(all_py_dict[p], is_pytype = True))
        st = len(utils.remove_keys_that_are_empty(all_dlgt_dict[p]))
        ml = len(utils.remove_keys_that_are_empty(all_dlml_dict[p]))
        dy = len(utils.remove_keys_that_are_empty(all_dldy_dict[p]))
        (a, b, c) = d["py"]
        data.append(["vs Pytype", pt, pyt, a + b + c, a, b, c])
        t_poto += pt; t_py += pyt; t_py_a += a; t_py_b += b; t_py_c += c
        (a, b, c) = d["st"]
        data.append(["vs DL-ST", pt, st, a + b + c, a, b, c])
        t_st += st; t_st_a += a; t_st_b += b; t_st_c += c 
        (a, b, c) = d["dy"]
        data.append(["vs DL-DY", pt, dy, a + b + c, a, b, c])
        t_dy += dy; t_dy_a += a; t_dy_b += b; t_dy_c += c
        (a, b, c) = d["ml"]
        data.append(["vs DL-ML", pt, ml, a + b + c, a, b, c])
        t_ml += ml; t_ml_a += a; t_ml_b += b; t_ml_c += c
        table = tabulate(data, headers = hd)
        print("=== {} ===".format(p))
        print(table, "\n")
    print("\n=== SUMMATION OF {} PACKAGES ===".format(len(all_packages)))
    data = []
    data.append(["vs Pytype", t_poto, t_py, t_py_a+t_py_b+t_py_c, t_py_a, t_py_b, t_py_c])
    data.append(["vs DL-ST", t_poto, t_st, t_st_a+t_st_b+t_st_c, t_st_a, t_st_b, t_st_c])
    data.append(["vs DL-DY", t_poto, t_dy, t_dy_a+t_dy_b+t_dy_c, t_dy_a, t_dy_b, t_dy_c])
    data.append(["vs DL-ML", t_poto, t_ml, t_ml_a+t_ml_b+t_ml_c, t_ml_a, t_ml_b, t_ml_c])
    table = tabulate(data, headers = hd)
    print(table, "\n")


def get_manual_verdict_all_techniques(current_dir: str, package: str, has_pytype_mv: bool) -> List[Dict]:
    path_py = current_dir + "stable_log/manual_verdict/Manual_verdict_PTplus_Pytype_" + package + ".txt"
    path_st = current_dir + "stable_log/manual_verdict/Manual_verdict_PTplus_DL-GT_" + package + ".txt"
    path_dy = current_dir + "stable_log/manual_verdict/Manual_verdict_PTplus_DL-DY_" + package + ".txt"
    path_ml = current_dir + "stable_log/manual_verdict/Manual_verdict_PTplus_Dl-ML_" + package + ".txt"
    if has_pytype_mv:
        mv_py = get_pytype_manual_verdict(package, path_py)
    else:
        mv_py = {}
    mv_st = get_DL_manual_verdict(package, path_st)
    mv_dy = get_DL_manual_verdict(package, path_dy)
    mv_ml = get_DL_manual_verdict(package, path_ml)
    return [mv_py, mv_st, mv_dy, mv_ml]

def get_pytype_manual_verdict(package: str, path: str) -> Dict:
    mv = {}
    with open(path, "r") as f:
        for line in f:
            line = line.replace("\n","")
            line = line.strip()
            l = line.split(" ")
            if len(l) != 3: continue
            k = (l[0], l[1])
            if k in mv: 
                assert False, "Duplicate in the manual verdict file"
            mv[k] = l[2]
    return mv

def get_DL_manual_verdict(package: str, path: str) -> Dict:
    mv = {}
    with open(path, "r") as f:
        for line in f:
            line = line.replace("\n","")
            if len(line) == 0: continue
            l = line.split(") ")
            assert len(l) == 2
            k = str_to_tuple(l[0])
            if k in mv:
                assert False, "Duplicate in the manual verdict file"
            mv[k] = l[1]
    return mv

def str_to_tuple(s):
    s = s.replace("(","").replace(")","")
    (a,b,c) = s.split(", ")
    a = a[1:-1]
    b = b[1:-1]
    c = c[1:-1]
    return (a, b, c)




if __name__ == "__main__":
    main(sys.argv[1:])




def get_poto_dict(package_name, current_dir):
    open_name = current_dir + "stable_log/" + "merged_poto_" + package_name + ".pkl"
    with open(open_name, 'rb') as f:
        pt_dict = pickle.load(f)
    return pt_dict

# side effect: populates global key_to_pt_table
def collect_pt_map(package_name, current_dir, key_to_pt_type):
    global use_stable_version
    if package_name != "ansible":
        pt_file_name = current_dir + "stable_log/" + "PTonly_" + package_name + ".txt"
        with open(pt_file_name, "r") as source:
            for line in source:
                if "typeshed" in line: continue
                pt_key = line[:line.find("[")-1]
                pt_value = line[line.find("["):-1]
                if "_ret')" in line and pt_value == "[None]": continue # Taking out return None's just as we do for Pytype
                if pt_value == "[]":
                    key_to_pt_type[pt_key] = []  
                else:    
                    #print("The pt value", pt_value, pt_value[1:-1])
                    key_to_pt_type[pt_key] = pt_value[1:-1].split(",,, ")
    else:
        # For ansible we read from 2 files
        pt_file_name = current_dir + "stable_log/" + "PTonly_" + package_name + "_part1.txt"
        pt_file_name_2 = current_dir + "stable_log/" + "PTonly_" + package_name + "_part2.txt"
        with open(pt_file_name, "r") as source:
            for line in source:
                if "typeshed" in line: continue
                pt_key = line[:line.find("[")-1]
                pt_value = line[line.find("["):-1]
                if "_ret')" in line and pt_value == "[None]": continue # Taking out return None's just as we do for Pytype
                if pt_value == "[]":
                    key_to_pt_type[pt_key] = []  
                else:    
                    #print("The pt value", pt_value, pt_value[1:-1])
                    key_to_pt_type[pt_key] = pt_value[1:-1].split(",,, ")
        with open(pt_file_name_2, "r") as source_2:
            for line in source_2:
                if "typeshed" in line: continue
                pt_key = line[:line.find("[")-1]
                pt_value = line[line.find("["):-1]
                if "_ret')" in line and pt_value == "[None]": continue # Taking out return None's just as we do for Pytype
                if pt_value == "[]":
                    key_to_pt_type[pt_key] = []  
                else:    
                    #print("The pt value", pt_value, pt_value[1:-1])
                    key_to_pt_type[pt_key] = pt_value[1:-1].split(",,, ")


"""
PT vs Pytype. Numbers OK!
- cerberus
- mtgjson
- pygal
- sc2
- zfsp
- wemake_python_styleguide

Pytype NOT MATCH (total/empty)
- anaconda 
    new run = 17912/10304
    spreadsheets = 17895/10312
- ansible
    new run = 18981/9614
    spreadsheets = 19018/9631
- bokeh
    new run = 14214/6382
    spreadsheets = 14223/6390
- invoke
    new run = 3349/1516
    spreadsheets = 3347/1516
"""

"""
    if False: # Old version
        # DL-GT, DL-DY, DL-ML
        #d = utils.get_dl_dict("DL-GT", "cerberus", current_dir)
        #print(len(d))

        d = utils.get_potoplus_dict_stable("cerberus")
        for k in d:
            print(k, d[k])
            x = k
        print(type(x), type(d[x]), type(d[x][0]))
        return False

        # PoTo
        missing_packages = ["bokeh", "invoke", "wemake_python_styleguide"]
        package_name = "cerberus"
        get_poto_dict(package_name, current_dir)


        global key_to_pt_type
        key_to_pt_type = {}
        collect_pt_map(package_name, current_dir, key_to_pt_type)
"""