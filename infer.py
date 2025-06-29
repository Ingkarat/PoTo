import json
import pickle
import ast
import os
import sys
import time
import shutil

import infer_shallow_type

use_stable_version = False

def main(argv):
    # TODO: Edit paths
    current_dir = ".../PoTo/"
    global use_stable_version
    use_stable_version = False

    # Should not have to edit this if using the default structure
    base_path_DLST = current_dir + "DLInfer_data/data/data_dynamic/static_json/"
    base_path_DLDY = current_dir + "DLInfer_data/data/data_dynamic/dynamic_json/"
    base_path_DLML = current_dir + "DLInfer_data/DLInfer_data/groud_truth_dynamic/"
    libraries = ["cerberus", "mtgjson", "pygal", "sc2", "zfsp", 
                "anaconda", "bokeh", "invoke", "wemake_python_styleguide"] # excluding ansible as it takes too long to run
    
    choice = 5

    # 1. Collect DLInfer ground truth information (DL-ST) which is a combination
    # of running the Pysonar2 static tool and extracting type information
    # Take up to couple minutes for large libraries ()
    if choice == 1:
        for lib_name in libraries:
            if lib_name != "cerberus": continue
            path_DLST = base_path_DLST + lib_name + ".json"
            path_DLML = base_path_DLML + lib_name + ".json"
            merge_two_DLInfer_json("ST", path_DLST, path_DLML, lib_name, current_dir)
    
    # 2. Collect DL-DY which is a set of dynamic type information obtained from executing
    # the test suites.
    # Similar to (1.)
    if choice == 2:
        for lib_name in libraries:
            if lib_name != "cerberus": continue
            path_DLDY = base_path_DLDY + lib_name + ".json"
            path_DLML = base_path_DLML + lib_name + ".json"
            merge_two_DLInfer_json("DY", path_DLDY, path_DLML, lib_name, current_dir)

    # 3. For DL-ML, the result of DLInfer's machine-learning approach, we retrieve it 
    # directly from the directory (/DLInfer_data/DLInfer_data/groud_truth_dynamic/)

    # 4. Export PoTo result into text file containing keys
    if choice == 4:
        for lib_name in libraries:
            if lib_name != "cerberus": continue
            if lib_name == "ansible": 
                ...
                #TODO: maybe we copy form the pre-run results?
            else:
                print_PT_in_this_format(lib_name, current_dir)

    # 5. Run Pytype to produce pytype types, then collect
    # then compare Poto+ with Pytype, DL-ST, DL-ML and DL-DY; result on stdout
    if choice == 5:
              
       package_name = "cerberus"
       
       run_Pytype(package_name,current_dir)       
       print("\n\nPTplus to Pytype Comparison:\n============================")
       compare_PTplus_Pytype(package_name,current_dir)
       print("\n\nPTplus to DL-ST Comparison:\n===========================")
       compare_PTplus_DL(package_name, current_dir, "DL-GT")
       print("\n\nPTplus to DL-ML Comparison:\n===========================")
       compare_PTplus_DL(package_name, current_dir, "DL-ML")
       print("\n\nPTplus to DL-DY Comparison:\n===========================")
       compare_PTplus_DL(package_name, current_dir, "DL-DY")


# This is the global map from abbrev_file_name -> { linenno -> var_name }. Reveals the variable at that specific line in file.  
lineno_to_var = {}
lineno_to_type = {}

# These are the important maps that we run comparisons on.
all_keys = [] # all keys. The 100% percent needed for coverage.
key_to_pytype = {}
key_to_pt_type = {}
# This maps files to functions contained in this file
file_to_funcs = {}

# For RQ3 G's suggestion
PoTo_Pytype_agree = {}
rq3_DL_total = 0
rq3_DL_key_in_PoToPytype_total = 0
rq3_DL_key_in_PoToPytype_match = 0
rq3_DL_key_in_PoToPytype_partial = 0
rq3_DL_key_in_PoToPytype_empty = 0
rq3_DL_key_in_PoToPytype_other = 0


# do this only once
def write_keys_ID(package_name, current_dir):
   new_dir = current_dir + "type_result/"
   if not os.path.exists(new_dir):
     os.makedirs(new_dir)
   if 1:
      path = current_dir + "type_result/Keys_ID_PTplus_" + package_name + ".txt"
      with open(path, "w") as f:
         i = 0
         for k in key_to_pt_type:
            print(i, k, file=f)
            i += 1
   path = current_dir + "type_result/Keys_ID_Pytype_" + package_name + ".txt"
   with open(path, "w") as f:
      i = 0
      for k in key_to_pytype:
         print(i, k, file=f)
         i += 1

# Run Pytype to produce pytype types, then collect: Step 1 and Step 2; this produces 
# instrumented code and pytype data in reveal_+CODE_DIR/package_name directory
# Next, collects pytype data in global key_to_pt_type: Step 3
# EFFECTS: populates globals key_to_pt_type and all_keys necessary for Poto comparisons
# EFFECTS: populates Keys_ID_ files
def run_Pytype(package_name, current_dir):

    # Setup for pytype run
    CODE_DIR = "orig_pro_dynamic"
    PYTYPE_OUTPUT_DIR = "./" + ".pytype" + "" + "/pyi"
    package_dir = CODE_DIR + "/" + package_name # modified /orig_pro_dynamic/ 
    package_pytype_dir = PYTYPE_OUTPUT_DIR 

    global key_to_pt_type
    key_to_pt_type = {}

    # Step 1: Transform (i.e., instrument) into parallell directory "instrumented_common_dir/..."
    print("Transforming libraries directory", CODE_DIR, "to reveal_"+CODE_DIR, "to prepare for pytype run")
    transform(current_dir,package_dir,package_name) 

    # Step 2: Run pytype on each file pytype k file_name
    # Collect into a common data structure
    start = time.time()
    print("Running pytype on each file (pytype -k FILENAME)")
    print("   only need to run once")
    collect_pytype(package_dir,package_name) # Expensive (run pytype here) # UNOCMMENT
    end = time.time()
    print(end - start, "seconds")
    # Collecting the return types into key_to_pytype
    print("Collecting return types from pytype'd files")
    collect_ret_pytypes(package_pytype_dir,package_name)
    end = time.time()
    print(end - start, "seconds")
    # Populating key_to_pytype with locals
    join_maps(package_name) 
    
    # Step 3: Collect PT from Bill's dumps and compare 
    collect_pt_map(package_name, current_dir, key_to_pt_type)
    len_key_to_pt_type_before = len(key_to_pt_type)
    print("Key_to_pt_type before:",len_key_to_pt_type_before)
    infer_shallow_type.infer(package_dir,package_name,key_to_pt_type)
    len_key_to_pt_type_after = len(key_to_pt_type)
    print("Key_to_pt_type after:",len_key_to_pt_type_after)
    print("Contribution of Poto+: ",(float)(len_key_to_pt_type_after - len_key_to_pt_type_before)/len_key_to_pt_type_after)
    print("all_keys =", len(all_keys))
    write_keys_ID(package_name, current_dir)

# REQUIRES: populated all_keys, pt_to_type, key_to_pytype
# REQUIRES: type_data/Manual_verdict_PTplus_Pytype* files
# EFFECTS: prints result to stdout (Coverage and Comparison RQs in paper)
def compare_PTplus_Pytype(package_name, current_dir):
   print_all_other = True
   path_PTplus_Keys_ID = current_dir + "type_result/Keys_ID_PTplus_" + package_name + ".txt"
   path_Pytype_Keys_ID = current_dir + "type_result/Keys_ID_Pytype_" + package_name + ".txt"
   d_id_key_PTplus = {}
   d_key_id_PTplus = {}
   d_id_key_Pytype = {}
   d_key_id_Pytype = {}
   with open(path_PTplus_Keys_ID, "r") as f:
      for line in f:
         # some faulty lines got in (somehow???)
         if "(" not in line and ")" not in line: continue
         idd = line[:line.find("(")-1]
         key = line[line.find("("):-1]
         if idd in d_id_key_PTplus: assert False
         d_id_key_PTplus[idd] = key
         if key in d_key_id_PTplus: assert False
         d_key_id_PTplus[key] = idd
   with open(path_Pytype_Keys_ID, "r") as f:
      for line in f:
         # some faulty lines got in (somehow???)
         if "(" not in line and ")" not in line: continue
         idd = line[:line.find("(")-1]
         key = line[line.find("("):-1]
         if idd in d_id_key_Pytype: assert False
         d_id_key_Pytype[idd] = key
         if key in d_key_id_Pytype: assert False
         d_key_id_Pytype[key] = idd

   path_manual_verdict = current_dir + "type_data/Manual_verdict_PTplus_Pytype_" + package_name + ".txt"
   # (#x, #y) -> #z
   # more info in note.txt in /pt_plusplus_data_compare/ directory
   manual_verdict = {}
   with open(path_manual_verdict, "r") as f:
      for line in f:
         line = line.replace("\n","")
         line = line.strip()
         l = line.split(" ")
         if len(l) != 3: continue
         k = (l[0], l[1])
         if k in manual_verdict: 
            print(k)
            assert False, "Duplicate in the manual verdict file"
         manual_verdict[k] = l[2]

   new_dir = current_dir + "type_result/"
   if not os.path.exists(new_dir):
     os.makedirs(new_dir)
   path_compare_exact = new_dir + "Compare_PTplus_Pytype_" + package_name + "_match.txt"
   path_compare_other = new_dir + "Compare_PTplus_Pytype_" + package_name + "_other.txt"
   both = 0
   exact = 0
   other = 0
   count = {}
   vv = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
   for v in vv:
    count[v] = 0
   count_sc2_ids = 0
   with open(path_compare_exact, "w") as f_ex, open(path_compare_other, "w") as f_ot, open("output.txt", "w") as f_f:
      for key in key_to_pt_type:
         if key in key_to_pytype:
            if key not in all_keys: continue
            if 0:
               if "sc2/ids/" in key:
                  if "module_initializer" in key or "_class_initializer" in key:
                     count_sc2_ids += 1
                     continue
            verdict = "?"
            both += 1
            # mostly the same as in equivalence()
            pt_type = []
            for x in key_to_pt_type[key]:
               if x.startswith('ANNO:'):
                  if x[5:] not in pt_type: pt_type.append(x[5:])
               else:
                  pt_type.append(x)   
            #pt_type = [x for x in key_to_pt_type[key] if not x.startswith('ANNO')]
            py_type = key_to_pytype[key] if is_any(str(key_to_pytype[key])) else [x for x in key_to_pytype[key] if not x == 'Any']
            verdict = get_verdict(pt_type, py_type, package_name)

            PTplus_id = d_key_id_PTplus[key]
            Pytype_id = d_key_id_Pytype[key]
            t = (PTplus_id, Pytype_id)
            #print(t)
            if t in manual_verdict:
               verdict = manual_verdict[t]
            assert verdict != "?"
            #print(PTplus_id, Pytype_id, verdict)
            #print(pt_type)
            #print(py_type)
            if verdict == "0" or verdict == "1":
               text = ""
               if verdict == "0": text = "(Match)"
               elif verdict == "1": text = "(Manual match)"
               else: assert False
               print("{}:".format(exact), key, PTplus_id, Pytype_id, verdict, text, file = f_ex)
               print("  PT:", pt_type, file = f_ex)
               print("  PY:", py_type, file = f_ex)
               exact += 1
            else:
               text = ""
               if verdict == "2": text = "(Both Empty)"
               elif verdict == "3": text = "(PT Empty)"
               elif verdict == "4": text = "(PY Empty (is_any() is true))"
               elif verdict == "5": text = "(PT subset PY)"
               elif verdict == "6": text = "(PY subset PT)"
               elif verdict == "7": text = "(etc)"
               elif verdict == "8": text = "(Partial match)"
               else: assert False
               if print_all_other: print_list = ["2", "3", "4", "5", "6", "7", "8"]
               else: print_list = ["5", "6", "7"]
               if verdict in print_list:
                  print("{}:".format(other), key, PTplus_id, Pytype_id, verdict, text, file = f_ot)
                  print("  PT:", pt_type, file = f_ot)
                  print("  PY:", py_type, file = f_ot)
               if verdict == "7":
                  print("{}:".format(other), key, PTplus_id, Pytype_id, verdict, text, file = f_f)
                  print("  PT:", pt_type, file = f_f)
                  print("  PY:", py_type, "\n",file = f_f)
               other += 1
            t = verdict
            if t not in count: assert False
            else:
               tt = count[t]
               tt += 1
               count[t] = tt
            
            if verdict == "1" or verdict == "0":
               PoTo_Pytype_agree[key] = pt_type

   # partial = partiaial and subsets
   partial = count["8"] + count["5"] + count["6"]
   empty = count["2"] + count["3"] + count["4"]
   other = count["7"]

   aa = 0
   for k in key_to_pt_type:
      if k in all_keys: aa += 1
   bb = 0
   for k in key_to_pytype:
      if k in all_keys: bb += 1

   print("TOTAL: PTplus = {}, {} = {}".format(aa, "Pytype", bb))
   print("both = {}\nboth MINUS either/both empty = {}\n exact = {}\n partial = {}\n other = {}".format(both, both - empty, exact, partial, other))
   
   print("TOTAL: PTplus = {}, {} = {}".format(aa, "Pytype", bb))
   print("both = {}\nboth MINUS either/both empty = {}\n exact = {}".format(both, both - empty, exact))
   print("  {} Match by code".format(count["0"]))
   print("  {} Match by manual verdict".format(count["1"]))
   print(" partial = {}".format(partial))
   print("  {} Some intersection".format(partial - count["5"] - count["6"]))
   print("  {} PTplus is subset of Pytype".format(count["5"]))
   print("  {} Pytype is subset of PTplus".format(count["6"]))
   print(" other = {}".format(other))
   print("empty = {}".format(empty))
   print(" {} Both empty".format(count["2"]))
   print(" {} PTplus empty".format(count["3"]))
   print(" {} Pytype empty".format(count["4"]))
   c1 = 0
   c2 = 0
   for k in key_to_pt_type:
      if k not in all_keys: continue
      if is_empty(key_to_pt_type[k]):
         c1 += 1
   for key in key_to_pytype:
      if key not in all_keys: continue
      pyy = py_type = key_to_pytype[key] if is_any(str(key_to_pytype[key])) else [x for x in key_to_pytype[key] if not x == 'Any']
      if is_any(str(pyy)):
         c2 += 1
      if key not in key_to_pt_type:
         if not is_any(str(pyy)):
            pass
            # print("ha ", key, pyy)
   print("\nPTplus overall empty = ", c1, "> total = ", aa)
   print("Pytype overall empty = ", c2, "> total = ", bb)
   #print(count_sc2_ids)
   print("{}    {}/{}/{}".format(exact+partial+other,exact,partial,other))

# DL-GT and DL-ST are used interchangeably. Will keep it as DL-GT here.
# DL-GT, DL-DY, DL-ML
# REQUIRES: globals all_keys, key_to_pt_type
# REQUIRES: dlinfer_result/*merged* files with DLInfer data, and type_data/Manual_verdict* files
# EFFECTS: prints comparison result to stdout
def compare_PTplus_DL(package_name, current_dir, mode_DL):
   #mode_DL = "DL-GT" # DLLLLLLL
   print_all_other = True

   use_manual_verdict = True
   bypass_all_keys_checking = False #TODO: MOSTLY WILL WANT THIS TO BE False

   path_DL = ""
   pt_dict = {}
   dl_dict = get_dl_dict(mode_DL, package_name, current_dir)
   print(package_name, len(dl_dict))

   global all_keys

   all_keys_tuple = []
   for k in all_keys:
      if (not k.startswith("(")) and (not k.endswith(")")): continue
      key = str_to_tuple(k)
      all_keys_tuple.append(key)

   for k in key_to_pt_type:
      if (not k.startswith("(")) and (not k.endswith(")")): continue
      key = str_to_tuple(k)
      pt_dict[key] = key_to_pt_type[k]
   
   if 0:
      ijk = 0
      print("PT_DICT")
      for k in pt_dict.keys():
         print(ijk, k)
         print(pt_dict[k],"\n")
         ijk += 1

   # RQ3
   global rq3_DL_total
   global rq3_DL_key_in_PoToPytype_total
   global rq3_DL_key_in_PoToPytype_partial
   global rq3_DL_key_in_PoToPytype_empty
   global rq3_DL_key_in_PoToPytype_match
   global rq3_DL_key_in_PoToPytype_other

   pt_and_dl = []  # (pt_key, pt_dict[pt_key], dl_key, dl_dict[dl_key])
   marked_pt = [] # mark pt_key that match with dl_key
   marked_dl = [] # mark dl_key that match with dl_key
   # New approach to deal with module/class init
   # match pt_dict's mod/class init to empty ("") function of dl_dict
   # O(NM) :(
   i = 0
   for p in pt_dict.keys():
      (a, b, c) = p
      for d in dl_dict.keys():
         (x, y, z) = d
         eq = False
         if p == d:
            eq = True
         else:
            if b == "module_initializer" or "_class_initializer" in b:
               if y == "":
                  if a == x and c == z:
                     eq = True
         if eq:
            i += 1
            #print("\n", i)
            #print(p)
            #print(d)
            item = (p, pt_dict[p], d, dl_dict[d])
            pt_and_dl.append(item)
            marked_pt.append(p)
            marked_dl.append(d)

   print(len(pt_dict), len(dl_dict), len(pt_and_dl))
   #assert False
   #print(current_dir)
   new_dir = current_dir + "type_result/"
   if not os.path.exists(new_dir):
     os.makedirs(new_dir)

   path_compare_exact = new_dir + "Compare_PTplus_" + mode_DL + "_" + package_name + "_match.txt"
   path_compare_other = new_dir + "Compare_PTplus_" + mode_DL + "_" + package_name + "_other.txt"
   both = 0
   exact = 0
   other = 0
   count = {}
   vv = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
   for v in vv:
    count[v] = 0

   path_manual_verdict = current_dir + "type_data/" + "Manual_verdict_PTplus_" + mode_DL + "_" + package_name + ".txt"
   manual_verdict = {}
   if use_manual_verdict:
      with open(path_manual_verdict, "r") as f:
         for line in f:
            line = line.replace("\n","")
            if len(line) == 0: continue
            l = line.split(") ")
            assert len(l) == 2
            k = str_to_tuple(l[0])
            if k in manual_verdict: 
               print(k)
               assert False, "Duplicate in the manual verdict file"
            manual_verdict[k] = l[1]

   count_sc2_ids = 0
   with open(path_compare_exact, "w") as f_ex, open(path_compare_other, "w") as f_ot, open("output.txt", "w") as f_f:
      for l in pt_and_dl:
         if not bypass_all_keys_checking:
            if l[0] not in all_keys_tuple: continue
         (p,pp,d,dd) = l

         if 0:
            (aa,bb,cc) = p
            if "/ids/" in aa:
               if bb == "module_initializer" or "_class_initializer" in bb:
                  count_sc2_ids += 1
                  continue

         both += 1
         verdict = "?"
         key = p
         pt_type = []
         for x in pp:
            if x.startswith('ANNO:'):
               if x[5:] not in pt_type: pt_type.append(x[5:])
            else:
               pt_type.append(x)  
         dl_type = dd
         verdict = get_verdict(pt_type, dl_type, package_name)

         if key in manual_verdict:
            verdict = manual_verdict[key]

         if verdict == "0" or verdict == "1":
            text = ""
            if verdict == "0": text = "(Match)"
            elif verdict == "1": text = "(Manual match)"
            else: assert False
            #print("{}:".format(exact), key, PTplus_id, Pytype_id, verdict, text, file = f_ex)
            print("{}:".format(exact), key, verdict, text, file = f_ex)
            print("  PT:", pt_type, file = f_ex)
            print("  DL:", dl_type, file = f_ex)
            exact += 1
         else:
            text = ""
            if verdict == "2": text = "(Both Empty)"
            elif verdict == "3": text = "(PT Empty)"
            elif verdict == "4": text = "(DL Empty)"
            elif verdict == "5": text = "(PT subset DL)"
            elif verdict == "6": text = "(DL subset PT)"
            elif verdict == "7": text = "(etc)"
            elif verdict == "8": text = "(Partial match)"
            else: assert False
            if print_all_other: print_list = ["2", "3", "4", "5", "6", "7", "8"]
            else: print_list = ["5", "6", "7"]
            if verdict in print_list:
               # print("{}:".format(other), key, PTplus_id, Pytype_id, verdict, text, file = f_ot)
               print("{}:".format(other), key, verdict, text, file = f_ot)
               print("  PT:", pt_type, file = f_ot)
               print("  DL:", dl_type, file = f_ot)
            if verdict == "7":
               print("{}:".format(other), key, verdict, text, file = f_f)
               print("  PT:", pt_type, file = f_f)
               print("  DL:", dl_type, "\n", file = f_f)
            other += 1
         t = verdict
         if t not in count: assert False
         else:
            tt = count[t]
            tt += 1
            count[t] = tt

         # RQ3
         rq3_DL_total += 1
         s = "{}".format(p)
         if s in PoTo_Pytype_agree:
            rq3_DL_key_in_PoToPytype_total += 1
            if verdict in ["8", "5", "6"]: rq3_DL_key_in_PoToPytype_partial += 1
            elif verdict in ["2", "3", "4"]: rq3_DL_key_in_PoToPytype_empty += 1
            elif verdict in ["0", "1"]: rq3_DL_key_in_PoToPytype_match += 1
            elif verdict in ["7"]: rq3_DL_key_in_PoToPytype_other += 1
            else: assert False

   # partial = partiaial and subsets
   partial = count["8"] + count["5"] + count["6"]
   empty = count["2"] + count["3"] + count["4"]
   other = count["7"]

   aa = 0
   for k in pt_dict:
      if bypass_all_keys_checking:
         aa += 1
      else:
         if k in all_keys_tuple: aa += 1
   bb = 0
   for k in dl_dict:
      if bypass_all_keys_checking:
         bb += 1
      else:
         if k in all_keys_tuple: bb += 1
      
   print("TOTAL: PTplus = {}, {} = {}".format(aa, mode_DL, bb))
   print("both = {}\nboth MINUS either/both empty = {}\n exact = {}\n partial = {}\n other = {}".format(both, both - empty, exact, partial, other))
   print("TOTAL: PTplus = {}, {} = {}".format(aa, mode_DL, bb))
   print("both = {}\nboth MINUS either/both empty = {}\n exact = {}".format(both, both - empty, exact))
   print("  {} Match by code".format(count["0"]))
   print("  {} Match by manual verdict".format(count["1"]))
   print(" partial = {}".format(partial))
   print("  {} Some intersection".format(partial - count["5"] - count["6"]))
   print("  {} PTplus is subset of DLtype".format(count["5"]))
   print("  {} DLtype is subset of PTplus".format(count["6"]))
   print(" other = {}".format(other))
   print("empty = {}".format(empty))
   print(" {} Both empty".format(count["2"]))
   print(" {} PTplus empty".format(count["3"]))
   print(" {} DLtype empty".format(count["4"]))
   c1 = 0
   c2 = 0

   for k in pt_dict:
      if not bypass_all_keys_checking:
         if k not in all_keys_tuple: continue
      if is_empty(pt_dict[k]):
         c1 += 1
   for k in dl_dict:
      if not bypass_all_keys_checking:
         if k not in all_keys_tuple: continue
      if is_empty(dl_dict[k]):
         c2 += 1
   print("\nPTplus overall empty = ", c1, "> total = ", aa)
   print(mode_DL, "overall empty = ", c2, "> total = ", bb)
   #print(count_sc2_ids)
   print("{}    {}/{}/{}".format(exact+partial+other,exact,partial,other))

   if 1:
      print(package_name)
      print("  ({}) {}/{}/{}".format(exact+partial+other, exact,partial,other))
      print("  ({}) {}/{}/{}".format(rq3_DL_key_in_PoToPytype_total-rq3_DL_key_in_PoToPytype_empty, rq3_DL_key_in_PoToPytype_match, rq3_DL_key_in_PoToPytype_partial, rq3_DL_key_in_PoToPytype_other))
      #print("  ({}) DL exact/partial/order = {}/{}/{}".format(exact+partial+other, exact,partial,other))
      #print("  ({}) DL that keys in [PoTo+_Pytype]'s match = {}/{}/{}".format(rq3_DL_key_in_PoToPytype_total, rq3_DL_key_in_PoToPytype_match, rq3_DL_key_in_PoToPytype_partial, rq3_DL_key_in_PoToPytype_other))


def get_verdict(pt_type, other_type, package_name):
   verdict = "?"
   if is_empty(pt_type) and is_any(str(other_type)): return "2"
   if is_empty(pt_type) and is_empty(other_type): return "2"
   if is_empty(pt_type): return "3"
   if is_any(str(other_type)): return "4"
   if is_empty(other_type): return "4"

   if str(pt_type) == str(other_type):
      return "0"
   
   printt = False
   if printt:
      print(len(pt_type))
      print(pt_type)
      print(other_type)
   
   pt_type = reconstruct(pt_type)
   other_type = reconstruct(other_type)

   ptt0 = []
   otherr0 = []
   ptt = []
   otherr = []
   dd = {"Dict": "dict",
         "Set[": "set",
         "Set(": "set",
         "List": "list",
         "Tuple": "tuple",
         "FrozenSet": "frozenset",
         "frozenset": "frozenset",
         "DefaultDict": "dict",
         "Mapping": "dict",
         "defaultdict": "dict",
         "collections.defaultdict": "dict",
         "OrderedDict": "dict",
         "ChainMap": "dict",
         "(dict_builtin)": "dict",
         "Sequence": "sequence",
         "Iterable": "iterable",
         "Iterator": "iterator",
         "Coroutine": "coroutine",
         "function": "meta_func",
         "callable": "meta_func",
         "Callable": "meta_func",
         "function": "meta_func",
         "<built-in function ": "meta_func",
         "<built-in method ": "meta_func",
         "<staticmethod ": "meta_func",
         "<bound method ": "meta_func",
         "<function ": "meta_func",
         "Generator": "generator",
         "re.compile": "regex",
         "re.Pattern": "regex",
         "<object object ": "object",
         "bytearray": "bytearray",
         "<ast.Module ": "ast.Module",
         "<module ": "module",
         "ArgumentParser": "argumentParser",
         "argparse.ArgumentParser": "argumentParser",
         "<configparser.ConfigParser": "ConfigParser",
         "configparser.ConfigParser": "ConfigParser",
         "argparse.Namespace": "namespace",
         "Namespace": "namespace",
         "NoneType": "None",
         "<Logger pt_engine": "logging",
         "logging.Logger": "logging",
         "<RootLogger ": "logging",
         "<logging.Formatter": "logging",
         "logging.Formatter": "logging",
         "operator.attrgetter": "operator.attrgetter",
         "operator.methodcaller": "operator.methodcaller",
         "/Users/ingkarat/Documents/GitHub/": "pathlib.Path",
         "/testpath": "pathlib.Path"}
   
   if package_name == "wemake_python_styleguide":
      ddd = {"FunctionCounter": "dict", 
            "FunctionCounterWithLambda": "dict",
            "FunctionNames": "dict",
            "typing_extensions.Final": "Final"}
      dd = dd | ddd

   def f_add_dd(x):
      for d in dd:
         if x.startswith(d): return dd[d]
      return x

   for a in pt_type:
      add = False
      for d in dd:
         if a.startswith(d):
            if dd[d] not in ptt0:
               ptt0.append(dd[d])
            add = True
            break
      if not add:
         if a not in ptt0:
            ptt0.append(a)
   for b in other_type:
      add = False
      for d in dd:
         if b.startswith(d):
            if dd[d] not in otherr0:
               otherr0.append(dd[d])
            add = True
            break
      if not add:
         if b not in otherr0:
            otherr0.append(b)
   for a in ptt0:
      if a not in ptt:
         ptt.append(a)
   for b in otherr0:
      if b not in otherr:
         otherr.append(b)

   if printt:
      print(ptt)
      print(otherr)

   #print("ptt ", ptt)
   #print("otherr ", otherr)

   # case that both len() = 1
   if len(ptt) == len(otherr) and len(ptt) == 1:
       # cases like   PT: ['ast.BinOp'], PY: ['_ast.BinOp'] 
       if ("_" + ptt[0]) == otherr[0]: return "0"
       if ptt[0] == ("_" + otherr[0]): return "0"
      

       # EXPERIMENTAL for cases like this
       # PT: ['Figure']
       # DL: ['bokeh.plotting.figure'] 
       if "." in otherr[0]:
          p = ptt[0]
          q = otherr[0].split(".")[-1]
          if p.lower() == q.lower():
             return "0"
       # PT: ['pt_engine.utils.base.Plugin']
       # DL: ['Type[Plugin]'] >> will become ['Plugin'] when it gets here
       if "." in ptt[0]:
          p = ptt[0].split(".")[-1]
          q = otherr[0]
          if p.lower() == q.lower():
             return "0"

   assert len(ptt) > 0 and len(otherr) > 0

   x_in_y = 0
   y_in_x = 0

   for a in ptt:
      if a in otherr:
            x_in_y += 1
   for b in otherr:
      if b in ptt:
            y_in_x += 1

   if x_in_y == 0 and y_in_x == 0: return "7"
   assert x_in_y != 0 and y_in_x != 0
   if len(ptt) == len(otherr):
      if x_in_y == y_in_x and x_in_y == len(ptt): return "0"
   if x_in_y == len(ptt): return "5"
   if y_in_x == len(otherr): return "6"
   return "8"

   if 0:
      print(ptt)
      print(otherr)
      print(verdict)

   return verdict


# Function that determins PT set empty.
def is_empty(type_str):
    if type_str == []: return True
    if len(type_str) == 1 and type_str[0] == "": return True
    if len(type_str) == 1 and type_str[0] == "Any": return True
    if len(type_str) == 1 and type_str[0] == "ANNO:Any": return True
    return False


# Function that determines Pytype set empty.    
def is_any(type_str):
    bad_types = ["['typing.Any']", "['nothing']", "['Any']", "['nothing', 'Any']", "['Any', 'nothing']", "['Optional[Any]']"]
    return str(type_str) in bad_types


def mod_string_change_outter_comma(s):
   bracket = 0
   ss = ""
   for a in s:
      if a == "[":
         bracket += 1
      elif a == "]":
         bracket -= 1
      if a == "," and bracket == 0:
         ss += ",,,"
      else:
         ss += a
   return ss


def stringlisthelper(s):
   s = mod_string_change_outter_comma(s)
   if ",,, " in s:
      s = s.replace(",,, ", ",,,")
   ss = s.split(",,,")
   return ss  

def reconstructOptional(ll):
   x = []
   for l in ll:
      if l.startswith("Optional["):
         a = l[9:-1]
         aa = stringlisthelper(a)
         for b in aa:
            x.append(b)
         x.append("None")
      else:
         x.append(l)
   return x

def reconstruct_ast(ll):
   x = []
   for l in ll:
      if l.startswith("_ast."):
         a = l[1:]
         x.append(a)
      else:
         x.append(l)
   return x

def reconstructClassVarORUnion(ll):
   x = []
   is_change = False
   for l in ll:
      if l.startswith("ClassVar["):
         a = l[9:-1]
         x.append(a)
         is_change = True
      elif l.startswith("Union["):
         a = l[6:-1]
         aa = stringlisthelper(a)
         for b in aa:
            x.append(b)
         is_change = True
      elif l.startswith("typing."):
         a = l[7:]
         x.append(a)
         is_change = True
      elif l.startswith("Type["):
         a = l[5:-1]
         x.append(a)
         is_change = True
      else:
         x.append(l)
   
   if is_change: return reconstructClassVarORUnion(x)

   # Type[Optional...  OR Optional[Type...  either can come first so here is an unsound (and bad) fix
   #return reconstructOptional(x)

   return x

def reconstruct(x):
   x = reconstructOptional(x)
   x = reconstructClassVarORUnion(x)
   x = reconstruct_ast(x)
   return x


def str_to_tuple(s):
   s = s.replace("(","").replace(")","")
   (a,b,c) = s.split(", ")
   a = a[1:-1]
   b = b[1:-1]
   c = c[1:-1]
   return (a, b, c)


def get_dl_dict(mode_DL, package_name, current_dir):
   dl_dict = {}
   if mode_DL == "DL-GT":
      path_DL = current_dir + "dlinfer_result/DL_merged_json_" + package_name + ".json"
   elif mode_DL == "DL-DY":
      path_DL = current_dir + "dlinfer_result/DL_dynamic_merged_json_" + package_name + ".json"
   elif mode_DL == "DL-ML":
      path_DL = current_dir + "DLInfer_data/DLInfer_data/groud_truth_dynamic/" + package_name + ".json"
   else:
      assert False
   with open(path_DL) as f:
      data = json.load(f)
      #print("data size =", len(data))
      for a, b in data.items():
         name = b["name"]
         file_path = b["file_path"]
         if mode_DL == "DL-ML":
            file_path = file_path.replace("orig_pro_dynamic/","")
         file_path = "!" + file_path
         file_path = file_path.replace("wemake-python-styleguide","wemake_python_styleguide")
         z_p_name = "!" + package_name
         file_path = file_path.replace(z_p_name,"")
         lineno = b["lineno"]
         if mode_DL == "DL-GT":
            type_ground = b["type_ground"]
         elif mode_DL == "DL-DY":
            type_dy = b["type_dy"]
         elif mode_DL == "DL-ML":
            typee = b["type"]
         else:
            type_ground = b["type_ground"]
         if mode_DL != "DL-ML":
            type_ML = b["type_ML"]
         func = b["func"]
         defclass = b["defclass"]
   
         if "/tests/" in file_path:
            continue
         if "/test/" in file_path:
            continue

         if func == "" and defclass == "":
            func = "module_initializer"
         
         if func == "" and defclass != "":
            func = defclass + "_class_initializer"
        
         key = (file_path, func, name)
         if mode_DL == "DL-GT":
            value = type_ground
         elif mode_DL == "DL-DY":
            value = type_dy
         elif mode_DL == "DL-ML":
            value = typee
         else:
            assert False

         if key not in dl_dict:
            dl_dict[key] = [value]
         else:
            #print("dupe K =", key)
            l = dl_dict[key]
            if value not in l:
               l.append(value)
               if len(l) >= 2 and "" in l:
                  l.remove("")
               dl_dict[key] = l
   #print("dl_dict size =", len(dl_dict), "(NVM IT"S BECAUSE THEY ARE IN /TESTS/ or /TEST/ DIR THAT WE DONT WANT after grouping duplicate keys = can be unsound)")
   return dl_dict


# side effect: populates global key_to_pt_table
def collect_pt_map(package_name, current_dir, key_to_pt_type):
   global use_stable_version
   if package_name != "ansible":
      print("Here and package is: ",package_name)
      pt_file_name = current_dir + "poto_result/" + "PTonly_" + package_name + ".txt"
      if use_stable_version:
        pt_file_name = current_dir + "pytype_data/stable_run_data/" + "PTonly_" + package_name + ".txt"
      with open(pt_file_name, "r") as source:
         for line in source:
            if "typeshed" in line: continue
            pt_key = line[:line.find("[")-1]
            pt_value = line[line.find("["):-1]
            if "_ret')" in line and pt_value == "[None]": continue # Taking out return None's just as we do for Pytype
            if pt_value == "[]":
               key_to_pt_type[pt_key] = []  
            else:    
               # print("The pt value", pt_value, pt_value[1:-1])
               key_to_pt_type[pt_key] = pt_value[1:-1].split(",,, ")
   else:
      # For ansible we read from 2 files
      pt_file_name = current_dir + "poto_result/" + "PTonly_" + package_name + "_part1.txt"
      pt_file_name_2 = current_dir + "poto_result/" + "PTonly_" + package_name + "_part2.txt"
      if use_stable_version:
        pt_file_name = current_dir + "pytype_data/stable_run_data/" + "PTonly_" + package_name + "_part1.txt"
        pt_file_name_2 = current_dir + "pytype_data/stable_run_data/" + "PTonly_" + package_name + "_part2.txt"
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

# because DL-ST and DL-DY is (almost 100%) a subset of DL-ML and we want 
# "func" and "defclass" information from DL-ML.
# This means we want to add "func" and "defclass" information to DL-ST and DL-DY.
# We do this by comparing
#   if name1 == name2 and lineno1 == lineno2 and file_path1 == mod_fp2:
# mode = ST or DY
def merge_two_DLInfer_json(mode, p1, p2, p_name, current_dir):
    # supposed to be their ground-truth
    # name, type, lineno, file_path (cerberus/setup.py)
    # p1 = ".../DLInfer_data/data/data_dynamic/static_json/cerberus.json"
    # p1 = ".../DLInfer_data/data/data_dynamic/dynamic_json/cerberus.json"

    # supposed to be their result of ML approach
    # name, type, lineno, func, defclass, file_path (orig_pro_dynamic/cerberus/setup.py), 
    # p2 = ".../DLInfer_data/DLInfer_data/groud_truth_dynamic/cerberus.json"

    data = {}
    i = 0
    iii = 0
    # First, match (name, lineno, file_path), then create (name, type, lineno, func, defclass, file_path)
    with open(p1) as fp1, open(p2) as fp2:
        data1 = json.load(fp1) 
        data2 = json.load(fp2)

        jjj = len(data1)

        # O(NM). Can probably sort and do some index slicing for O(N+M) matching but whatever
        for a1, b1 in data1.items():
            name1 = b1["name"]
            type1 = b1["type"]
            lineno1 = b1["lineno"]
            file_path1 = b1["file_path"]

            iii += 1
            if iii % 100 == 0:
                print("{}: processing {} out of {} data".format(p_name, iii, jjj))

            for a2, b2 in data2.items():
                name2 = b2["name"]
                type2 = b2["type"]
                lineno2 = b2["lineno"]
                func = b2["func"]
                defclass = b2["defclass"]
                file_path2 = b2["file_path"]
                mod_fp2 = file_path2.replace("orig_pro_dynamic/","")

                if name1 == name2 and lineno1 == lineno2 and file_path1 == mod_fp2:
                    i += 1
                    d = {}
                    d["name"] = name1
                    d["file_path"] = file_path1
                    d["lineno"] = lineno1
                    if mode == "DY":
                        d["type_dy"] = type1
                    elif mode == "ST":
                        d["type_ground"] = type1
                    else:
                        assert False
                    d["type_ML"] = type2
                    d["func"] = func
                    d["defclass"] = defclass
                    data[str(i)] = d

    # cerberus_merged_json.json
    new_dir = current_dir + "dlinfer_result/"
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    if mode == "ST":
        write_path = new_dir + "DL_merged_json_" + p_name + ".json"
    elif mode == "DY":
        write_path = new_dir + "DL_dynamic_merged_json_" + p_name + ".json"
    else:
        assert False
    with open(write_path, "w") as f:
        print ("HERE,",f)
        json.dump(data, f)
    print(p_name, len(data))


def process_type_indiv(x):
    if x == 'None': return x
    if x == 'int': return x
    if x == 'float': return x
    if x == 'bool': return x
    if x == 'str': return x
    if x == 'list': return x
    if x == 'tuple': return x
    if x == 'set': return x
    if x == 'dict': return x

    # new constant format
    if 'string(c_int' in x: return 'int'
    if 'string(c_none' in x: return 'None'
    if 'string(c_str' in x: return 'str'
    if 'string(c_bool' in x: return 'bool'
    if 'string(c_float' in x: return 'float'
    if 'string(c_bytes' in x: return 'bytes'
    if 'string(c_complex' in x: return 'complex'
    if 'string(c_)' in x:
        print(x)
        assert False, "constant in the form of string(c_ in x"

    # TODO: REALLY need to double check this
    # result from concrete evaluation. proto|(...) or proto|{...} or 
    # if x == 'proto|()' or x == 'proto|{}' or x == 'proto|[]': return ""
    # proto|<class 'str'>, proto|<class 'tuple'>, etc
    if 'proto|<class \'' in x:
        xx = x.replace("proto|<class \'", "")
        return xx.replace("\'>", "")

    if 'proto|' in x:
        z = x.replace("proto|","")
        try:
            y = ast.literal_eval(z) # is this dangerous?
            #print(x)
            if isinstance(y, bool): return 'bool'
            elif isinstance(y, dict): return 'dict'
            elif isinstance(y, float): return 'float'
            elif isinstance(y, frozenset): return 'frozenset'
            elif isinstance(y, int): return 'int'
            elif isinstance(y, list): return 'list'
            elif isinstance(y, map): return 'map'
            elif isinstance(y, set): return 'set'
            elif isinstance(y, str): return 'str'
            elif isinstance(y, tuple): return 'tuple'
        except:
            ...
        #print("> ", x)
        #assert False
    #if 'proto|{' in x:
        # DANGER. {1} is set
    #    return 'dict'
    # TODO: check this. TUPLE ???
    if 'proto|(' in x: return 'tuple'
    if 'proto|[' in x: return 'list'
    # DANGER. {1} is set (but it should be resolved in the try-catch above?)
    if 'proto|{' in x: return 'dict'
    if 'proto|' in x:
        return x.replace("proto|", "")


    if x == 'string': return 'str'
    #if 'string(c_' in x: return 'str'
    if 'proto' in x: 
        return x
    if '(list_builtin)' in x: return 'list'
    if '(tuple_builtin)' in x: return 'tuple'
    if '(dict_builtin)' in x: return 'dict'
    if 'set()' in x: return 'set'

    sp = x.split("|")
    if len(sp) > 1:
        if 'meta_func' in sp[0]: return 'meta_func'
        if 'meta_cls' in sp[0]: 
            #return 'meta_cls'
            return sp[-1]
        if ')user' in sp[0]:
            return sp[0].replace(")user","").replace("(","")


    # DLInfer stuff
    if x == "definition": return x
    if "cerberus.base" in x: return x
    if "value" in x: return x
    if "collections." in x: return x
    if x == "(None,None,None,None,None)": return 'None'
    if x == "min": return x

    print("\n>> ", x,"\n")
    assert False

def list_to_text(L):
    ret = ""
    lenn = len(L)
    i = 0
    for l in L:
        if l is None:
            ret += "NoneType"
        else:
            ret += l
        if i < lenn - 1:
            ret += " | "
        i += 1
    return ret

def process_type_list(L):
    ret = []
    for ll in L:
        t = process_type_indiv(ll)
        if t == "": continue
        if t not in ret:
            ret.append(t)
    try:
        ret.sort()
    except:
        x = 1
    return list_to_text(ret)

def print_PT_in_this_format(p_name, current_dir):
    # PT aggregated results        merged_cerberus_no_tests.pkl
    #open2_name = "NEW_merged_" + p_name + "_no_tests.pkl"
    open2_name = current_dir + "poto_result/" + "merged_poto_" + p_name + ".pkl"
    out_path = current_dir + "poto_result/" + "PTonly_" + p_name + ".txt"
    with open(open2_name, 'rb') as f:
        pt_dict = pickle.load(f)

    emp = 0
    with open(out_path, "w") as file:
        for p in pt_dict.keys():
            x = pt_dict[p]
            (a,b,c) = p # (file, func, var)
            l = process_type_list(x)
            l = l.replace(" | ", ",,, ")
            l = "["  + l + "]"
            #print("\t", x)
            if len(x) == 0: emp += 1
            print(p,l, file=file)
    print("{}: Export keys of PoTo result to PTonly_XXX.txt. {} keys, {} empty".format(p_name, len(pt_dict), emp))
    #print(len(pt_dict), emp)



# Start of add_reaveal_type
class CollectLocalVars(ast.NodeVisitor):
   def __init__(self,node):
      assert isinstance(node,ast.FunctionDef) or isinstance(node,ast.AsyncFunctionDef), "node not a FunctionDef"
      self.local_vars = []
      self.has_ret = False
      self.lhs_flag = False
      self.nested_func = False
      # Adding all param names
      all_params = node.args.posonlyargs + node.args.args + node.args.kwonlyargs + [node.args.vararg] + [node.args.kwarg]
      for param in all_params:
         if param != None:
             self._add_to_local_vars(param.arg)
             #if hasattr(param,"annotation"): delattr(param,"annotation") # Removing annotations

   def _add_to_local_vars(self,var_name):
      if var_name not in self.local_vars: self.local_vars.append(var_name)
   def _process_assign(self,lhs,rhs):
      self.lhs_flag = True
      if isinstance(lhs,list):
        for target in lhs:
            self.visit(target)
      else:
        self.visit(lhs)
      self.lhs_flag = False
      if rhs != None: self.visit(rhs)

   def visit_Assign(self,node):
      self._process_assign(node.targets,node.value)

   def visit_AugAssign(self,node):
      self._process_assign(node.target,node.value)

   def visit_AnnAssign(self,node):
      self._process_assign(node.target,node.value)

   def visit_For(self,node):
      # To collect the target nodes 
      self.generic_visit(node)
      self.lhs_flag = True
      if node.target != None: self.visit(node.target)
      self.lhs_flag = False

   def visit_comprehension(self,node):
      #self.generic_visit(node)
      self.lhs_flag = True
      if node.target != None: self.visit(node.target)
      self.lhs_flag = False
   
   def visit_Return(self,node):
      if node.value != None:
         self.has_ret = True

   def visit_Attribute(self,node):
      pass
   def visit_Subscript(self,node):
      pass
   def visit_Name(self,node):
      # If attribute flag is on, record name in local_vars
      if self.lhs_flag == True:
          if node.id not in self.local_vars: self.local_vars.append(node.id) 

   # To collect the inner function name...
   def visit_FunctionDef(self,node):      
      if self.nested_func == False:
         self.nested_func = True
         self.generic_visit(node)
      else:
         pass   
         #print("Found a nested func: ", node.name)
         #if node.name not in self.local_vars: self.local_vars.append(node.name)
   def visit_AsyncFunctionDef(self, node):
      self.visit_FunctionDef(node)

class TransformVisitor(ast.NodeVisitor):
    def __init__(self,file_name,package_name):
        self.file_name = file_name
        self.package_name = package_name
        self.module = None
        self.class_def = []
        self.module_init_vars = []
        self.class_init_vars = []
        self.lhs_flag = False
        self.func_def = []
    
    # Code below is solely for the purpose of handling Assigns in module initializers; repeats collection code 
    def _add_to_vars(self,var_list,var_name):
      if var_name not in var_list: var_list.append(var_name)
    def _process_assign(self,lhs,rhs):
      self.lhs_flag = True
      if isinstance(lhs,list):
        for target in lhs:
            self.visit(target)
      else:
        self.visit(lhs)
      self.lhs_flag = False
      if rhs != None: self.visit(rhs)

    def visit_Assign(self,node):
      self._process_assign(node.targets,node.value)

    def visit_AugAssign(self,node):
      self._process_assign(node.target,node.value)

    def visit_AnnAssign(self,node):
      self._process_assign(node.target,node.value)

    def visit_Attribute(self,node):
      pass
    def visit_Subscript(self,node):
      pass
    def visit_Name(self,node):
      # If attribute flag is on, record name in local_vars
      if self.func_def == [] and self.lhs_flag == True:
          if self.class_def == []: # We are in a module
             self._add_to_vars(self.module_init_vars,node.id)
          else:
             self._add_to_vars(self.class_init_vars[-1],node.id)
    
    def _insert_reveal_var(self,body,var,pos=None):
       the_stmt_str = "reveal_type("+var+")"
       if pos == None: body.append(ast.parse(the_stmt_str))
       else: body.insert(pos,ast.parse(the_stmt_str))

    # With side effects on module body
    def visit_Module(self,node):
       self.generic_visit(node)
       for var in self.module_init_vars:
          self._insert_reveal_var(node.body,var)
       # Replacing AnnAssign with Assign to Removing annotation
       # node.body = [self._replace_ann_assign(stmt) if isinstance(stmt,ast.AnnAssign) else stmt for stmt in node.body]   

    # With side effects
    def visit_ClassDef(self,node):
        self.class_def.append(node)
        self.class_init_vars.append([])
        self.generic_visit(node)
        for var in self.class_init_vars[-1]:
            self._insert_reveal_var(node.body,var)
        self.class_def = self.class_def[:-1] # pop
        self.class_init_vars = self.class_init_vars[:-1] # popping off
        # One idea: simply drop AnnAssign x : Ann (i.e., value == None) class inits. Removing AnnAssign class init annotations
        #node.body = [stmt if not isinstance(stmt,ast.AnnAssign) else (self._replace_ann_assign(stmt) if stmt.value != None else None) for stmt in node.body]
        #node.body = [x for x in node.body if x != None]

    # Will side-effect node with additional stmts
    def visit_FunctionDef(self,node):
        # print("FUNCTION DEF HERE in "+node.name)
        self.func_def.append(node)
        self.generic_visit(node) # NEW: Will visit and instrument into nested functions
        self.func_def = self.func_def[:-1]
        local_vars_visitor = CollectLocalVars(node)
        local_vars_visitor.visit(node)
        #if hasattr(node,"returns"): delattr(node,"returns") # Removing return annotation 
        if self.file_name not in file_to_funcs: file_to_funcs[self.file_name] = []
        if node.name not in file_to_funcs[self.file_name]: file_to_funcs[self.file_name].append(node.name)
        if local_vars_visitor.has_ret == True: # if isinstance(node.body[-1],ast.Return): # or isinstance(node.body[-1],ast.If):
           for local_var in local_vars_visitor.local_vars:
                self._insert_reveal_var(node.body,local_var,pos=-1)
        else:
           for local_var in local_vars_visitor.local_vars:
                self._insert_reveal_var(node.body,local_var)
        # Replacing AnnAssign with Assign. Removing annotation
        # node.body = [self._replace_ann_assign(stmt) if isinstance(stmt,ast.AnnAssign) else stmt for stmt in node.body]        

    def _replace_ann_assign(self,ann_assign):
       #print("ANN ASSIGN: ", ast.dump(ann_assign), ann_assign.lineno, ann_assign.col_offset)
       #print("ANN ASSIGN unparse: ", ast.unparse(ann_assign))
       lhs = ast.unparse(ann_assign.target)
       rhs = ast.unparse(ann_assign.value) if (hasattr(ann_assign,"value") and ann_assign.value != None) else "None"
       assign_str = lhs + " = " + rhs
       return ast.parse(assign_str)

    # Will side effect node 
    def visit_AsyncFunctionDef(self,node):
        self.visit_FunctionDef(node)
        #print("HERE in ",node.name)
         

class GrabRevealVisitor(ast.NodeVisitor):
   def __init__(self,file_name,package_name):
      self.file_name = file_name # For module initializers
      self.package_name = package_name
      self.encl_func_name = [] # For local vars
      self.encl_class_name = [] # For class initializers
   
   def _add_to_map(self, the_lineno, the_var_name):
      if self.file_name not in lineno_to_var:
         lineno_to_var[self.file_name] = {}  
      lineno_to_var[self.file_name][the_lineno] = the_var_name  

   def _make_name(self,var_name):
      if self.encl_func_name != []: # then it's a local var
         return "('" + self.file_name + "', '" + self.encl_func_name[-1] + "', '" + var_name +"')"    
      elif self.encl_class_name != []: # then it's a class initializer
         class_init_portion = "('" + self.file_name + "', '" + self.encl_class_name[-1]+"_class_initializer" + "', '" + var_name +"')"
         other_portion = "('" + self.file_name + "', '" + "', '" + var_name +"')" 
         return class_init_portion #+ " " + other_portion
      else: # if both are empty then it is a module init
         module_init_portion = "('" + self.file_name + "', '" + "module_initializer" + "', '" + var_name +"')"
         other_portion = "('" + self.file_name + "', '" + "', '" + var_name +"')" 
         return module_init_portion #+ " " + other_portion
   
   def visit_ClassDef(self,node):
      self.encl_class_name.append(node.name) # push on stack
      self.generic_visit(node)
      self.encl_class_name = self.encl_class_name[:-1]

   def visit_FunctionDef(self,node):
      self.encl_func_name.append(node.name) # push
      self.generic_visit(node)
      self.encl_func_name = self.encl_func_name[:-1] # pop

   def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
      self.visit_FunctionDef(node)

   def visit_Call(self,node):
      if isinstance(node.func,ast.Name) and node.func.id == "reveal_type":
          var_name = ast.unparse(node)[ast.unparse(node).find('(')+1:ast.unparse(node).find(')')]
          #self._add_to_map(node.lineno,self._make_local_name(self.encl_func_name[-1],var_name))   
          self._add_to_map(node.lineno,self._make_name(var_name))       
          if self._make_name(var_name) not in all_keys: all_keys.append(self._make_name(var_name))

   def visit_Return(self,node):
      cand = self._make_name(self.encl_func_name[-1]+"_ret")
      if cand not in all_keys: all_keys.append(cand)       

def transform(current_dir, package_dir, package_name):
  new_dir = current_dir + "reveal_orig_pro_dynamic/"
  if not os.path.exists(new_dir):
    shutil.copytree(current_dir + "orig_pro_dynamic", new_dir, dirs_exist_ok=True)
  for path, directory, files in os.walk(package_dir):
    for file in files:
      if file.endswith(".py"):
        file_name = os.path.join(path, file).replace("\\","/").replace("C:","") # remove "C:" to avoid split() issue
        if "/tests/" in file_name: continue # Skipping analysis of test files
        if "/test/" in file_name: continue # Skipping analysis of test files
        #if "base.py" not in file_name: continue 
        #print(file_name)
        #print(package_dir)
        #print(len(package_dir))
        abbrev_file_name = file_name[len(package_dir):]
        #print("abbrev: ", abbrev_file_name)
        #print("Transforming: ",file_name)
        s = file_name
        reveal_file_name = s.replace("orig_pro_dynamic", "reveal_orig_pro_dynamic")
        print("Will write into:",reveal_file_name )
        #assert False
        transform_visitor = TransformVisitor(abbrev_file_name,package_name)
        reveal_visitor = GrabRevealVisitor(abbrev_file_name,package_name)
        try:
          with open(file_name, "r") as source, open(reveal_file_name , "w") as target:   
            tree = ast.parse(source.read(), type_comments=True, feature_version=sys.version_info[1])
            transform_visitor.visit(tree)
            target.write(ast.unparse(tree))
          with open(reveal_file_name , "r") as target1:  
            reveal_tree = ast.parse(target1.read(), type_comments=True, feature_version=sys.version_info[1])
            reveal_visitor.visit(reveal_tree)
        except SyntaxError:
          #print("Oops, Syntax error: ")
          ...
        #print("Done transforming: ",file_name)
  #for file_key in lineno_to_var:
  #  print("lineno_to_var HERE IS THE FILE "+file_key)
  #  for lineno in lineno_to_var[file_key]:
  #    print("  "+str(lineno)+": "+str(lineno_to_var[file_key][lineno]))   

def collect_ret_pytypes(package_dir, package_name):
   
   class CollectRetVisitor(ast.NodeVisitor):
    
    def __init__(self,file_name,package_name):
       self.file_name = file_name
       self.package_name = package_name
       self.encl_class_name = None

    def visit_ClassDef(self,node):
       self.encl_class_name = node.name
       self.generic_visit(node)

    def visit_FunctionDef(self,node):
       if self.file_name not in file_to_funcs: return
       if node.name not in file_to_funcs[self.file_name]: return
       ret_type = ast.unparse(node.returns)
       #print("file name", self.file_name)
       if ret_type in ["builtins.NoneType", "None"]: # or ret_type.startswith("_"):
          return
       #print(node.name + " returns " + ret_type) 
       key = "(\'" + self.file_name + "\', \'" + node.name + "\', \'" +node.name+"_ret\')"
       if key not in key_to_pytype: key_to_pytype[key] = []
       if ret_type not in key_to_pytype[key]: key_to_pytype[key].append(ret_type)

    def visit_AsyncFunctionDef(self,node):
       self.visit_FunctionDef(node)   

   #print("\nHERE IN collect ret pytypes ",package_dir)
   for path, directory, files in os.walk(package_dir):
    for file in files:
      if file.endswith(".pyi"):
        #print("Collecting ret types from ",file)
        file_name = os.path.join(path, file).replace("\\","/").replace("C:","") # remove "C:" to avoid split() issue
        #print("After join file name is ",file_name, "and package name is", package_dir)
        #abbrev_file_name = file_name[len(".pytype/pyi"):-1]
        #file_name.replace("orig_pro_dynamic",".pytype/pyi")
        #old_abbrev_file_name = file_name[len(".pytype_"+package_name+"/pyi"):-1]
        #print("1", file_name)
        #abbrev_file_name = file_name.split(".pytype_"+package_name+"/pyi")[-1][:-1]
        abbrev_file_name = file_name.split(".pytype"+""+"/pyi")[-1][:-1]
        print("2", abbrev_file_name)
        #file_name.replace("orig_pro_dynamic",".pytype_"+package_name+"/pyi")
        file_name.replace("orig_pro_dynamic",".pytype"+""+"/pyi")
        print("3", file_name)
        
        collect_ret_visitor = CollectRetVisitor(abbrev_file_name,package_name)
        #print("Collecting rets from ",file_name, "and abbrev filename", abbrev_file_name)
        try:
           with open(file_name, "r") as source:   
             tree = ast.parse(source.read(), type_comments=True, feature_version=sys.version_info[1])
             collect_ret_visitor.visit(tree)
        except SyntaxError:
           #print("???")
           pass
        #print("Done collecting ret from ",file_name)

def _add_to_map(the_map,file_name,lineno,pytype):
   if file_name not in the_map:
      the_map[file_name] = {}
   lineno_map = the_map[file_name]
   if lineno not in lineno_map:
      lineno_map[lineno] = []
   type_list = lineno_map[lineno]
   if pytype not in type_list: type_list.append(pytype)      


def collect_pytype(package_dir, package_name):
   iii = 0
   for path, directory, files in os.walk(package_dir):
    for file in files:
      if file.endswith(".py"):
        file_name = os.path.join(path, file).replace("\\","/").replace("C:","") # remove "C:" to avoid split() issue
        if "/tests/" in file_name: continue # Skipping analysis of test files
        if "/test/" in file_name: continue # Skipping analysis of test files
        abbrev_file_name = file_name[len(package_dir):]       
        #print(file_name)
        #print(abbrev_file_name)
        s = file_name
        ss = file_name
        rev_file_name_rev = s.replace("orig_pro_dynamic", "reveal_orig_pro_dynamic") + "_reveal_pytype_result"
        #print(rev_file_name_rev)
        #assert False
        print(iii, "Running pytype on: ","reveal_"+file_name)
        iii += 1
        os.system("pytype -k reveal_"+file_name+" | grep \"\[reveal-type\]\" > reveal_"+file_name+"_reveal_pytype_result")
        try: 
          with open(rev_file_name_rev, "r") as target:
            for line in target:
               lineno = int(line[line.find(', line ')+7:line.find(", in ")])
               pytype = line[line.find(": ")+2:line.find(" [reveal-type]")]
               #print("line and pytype and abbrev_file_name",lineno,pytype,abbrev_file_name)
               _add_to_map(lineno_to_type,abbrev_file_name,lineno,pytype) 
        except SyntaxError:
          #print("OOPS") 
          ...      
        #print("Done collecting pytypes: ",file_name)   
   #for file_key in lineno_to_type:
   # print("HERE IS THE FILE "+file_key)
   # for lineno in lineno_to_type[file_key]:
   #     print("  "+str(lineno)+": "+str(lineno_to_type[file_key][lineno]))   

# side effect key_to_pytype: joins lineno_to_var and lineno_to_type 
def join_maps(package_name):
   # collecting the pytype table 
   for file_key in lineno_to_type:
    #print("Here in join_map file_key", file_key)
    lineno_to_var_m = lineno_to_var[file_key]
    lineno_to_type_m = lineno_to_type[file_key]
    for lineno in lineno_to_type_m:
       key = lineno_to_var_m[lineno]
       key_to_pytype[key] = []
       for pytype in lineno_to_type_m[lineno]:
          if pytype not in key_to_pytype[key]: key_to_pytype[key].append(pytype)

if __name__ == "__main__":
    main(sys.argv[1:])
